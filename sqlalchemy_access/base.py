# access/base.py
# Copyright (C) 2007-2012 the SQLAlchemy authors and contributors <see AUTHORS file>
# Copyright (C) 2007 Paul Johnston, paj@pajhome.org.uk
# Portions derived from jet2sql.py by Matt Keranen, mksql@yahoo.com
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""
Support for the Microsoft Access database.


"""
from sqlalchemy import sql, schema, types, exc, pool
from sqlalchemy.sql import compiler, expression
from sqlalchemy.engine import default, base, reflection
from sqlalchemy import processors

import pyodbc

ischema_names = {
    'INTEGER': types.Integer,
    'SMALLINT': types.SmallInteger,
    'NUMERIC': types.Numeric,
    'FLOAT': types.Float,
    'DATETIME': types.DateTime,
    'DATE': types.Date,
    'TEXT': types.String,
    'BINARY': types.LargeBinary,
    'YESNO': types.Boolean,
    'CHAR': types.CHAR,
    'TIMESTAMP': types.TIMESTAMP,
}

odbc_column_types = {
    pyodbc.SQL_BIT: types.Boolean,
    pyodbc.SQL_CHAR: types.CHAR,
    pyodbc.SQL_DOUBLE: types.Float,
    pyodbc.SQL_FLOAT: types.Float,
    pyodbc.SQL_INTEGER: types.Integer,
    pyodbc.SQL_LONGVARBINARY: types.LargeBinary,
    pyodbc.SQL_NUMERIC: types.Numeric,
    pyodbc.SQL_SMALLINT: types.SmallInteger,
    pyodbc.SQL_TYPE_DATE: types.Date,
    pyodbc.SQL_TYPE_TIMESTAMP: types.DateTime,
    pyodbc.SQL_WVARCHAR: types.String,
    -10: types.CLOB,  # reported by Access ODBC as LONGCHAR for "Long Text" (Memo) fields
}


class AcNumeric(types.Numeric):
    def get_col_spec(self):
        return "NUMERIC"

    def bind_processor(self, dialect):
        return processors.to_str

    def result_processor(self, dialect, coltype):
        return None


class AcFloat(types.Float):
    def get_col_spec(self):
        return "FLOAT"

    def bind_processor(self, dialect):
        """By converting to string, we can use Decimal types round-trip."""
        return processors.to_str


class AcInteger(types.Integer):
    def get_col_spec(self):
        return "INTEGER"


class AcTinyInteger(types.Integer):
    def get_col_spec(self):
        return "TINYINT"


class AcSmallInteger(types.SmallInteger):
    def get_col_spec(self):
        return "SMALLINT"


class AcDateTime(types.DateTime):
    def get_col_spec(self):
        return "DATETIME"


class AcDate(types.Date):
    def get_col_spec(self):
        return "DATETIME"


class AcText(types.Text):
    def get_col_spec(self):
        return "MEMO"


class AcString(types.String):
    def get_col_spec(self):
        return ("TEXT(%d)" % self.length) if self.length in range(1, 256) else "MEMO"


class AcUnicode(types.Unicode):
    def get_col_spec(self):
        return ("TEXT(%d)" % self.length) if self.length in range(1, 256) else "MEMO"

    def bind_processor(self, dialect):
        return None

    def result_processor(self, dialect, coltype):
        return None


class AcChar(types.CHAR):
    def get_col_spec(self):
        return ("TEXT(%d)" % self.length) if self.length in range(1, 256) else "MEMO"


class AcBinary(types.LargeBinary):
    def get_col_spec(self):
        return "BINARY"


class AcBoolean(types.Boolean):
    def get_col_spec(self):
        return "YESNO"


class AcTimeStamp(types.TIMESTAMP):
    def get_col_spec(self):
        return "TIMESTAMP"


class AccessExecutionContext(default.DefaultExecutionContext):
    def get_lastrowid(self):
        self.cursor.execute("SELECT @@identity AS lastrowid")
        return self.cursor.fetchone()[0]


class AccessCompiler(compiler.SQLCompiler):
    extract_map = compiler.SQLCompiler.extract_map.copy()
    extract_map.update({
            'month': 'm',
            'day': 'd',
            'year': 'yyyy',
            'second': 's',
            'hour': 'h',
            'doy': 'y',
            'minute': 'n',
            'quarter': 'q',
            'dow': 'w',
            'week': 'ww'
    })

    def visit_cast(self, cast, **kwargs):
        return cast.clause._compiler_dispatch(self, **kwargs)

    def get_select_precolumns(self, select, **kw):
        # (plagiarized from mssql/base.py)
        """ Access puts TOP, it's version of LIMIT here """

        s = ""
        if select._distinct:
            s += "DISTINCT "

        if select._simple_int_limit and not select._offset:
            # ODBC drivers and possibly others
            # don't support bind params in the SELECT clause on SQL Server.
            # so have to use literal here.
            s += "TOP %d " % select._limit

        if s:
            return s
        else:
            return compiler.SQLCompiler.get_select_precolumns(
                self, select, **kw
            )

    def limit_clause(self, select):
        """Limit in access is after the select keyword"""
        return ""

    def binary_operator_string(self, binary):
        """Access uses "mod" instead of "%" """
        return binary.operator == '%' and 'mod' or binary.operator

    function_rewrites = {'current_date': 'now',
                          'current_timestamp': 'now',
                          'length': 'len',
                          }

    def visit_function(self, func, **kwargs):
        """Access function names differ from the ANSI SQL names;
        rewrite common ones"""
        func.name = self.function_rewrites.get(func.name, func.name)
        return super(AccessCompiler, self).visit_function(func)

    def for_update_clause(self, select):
        """FOR UPDATE is not supported by Access; silently ignore"""
        return ''

    # Strip schema
    def visit_table(self, table, asfrom=False, **kwargs):
        if asfrom:
            return self.preparer.quote(table.name, table.quote)
        else:
            return ""

    def visit_join(self, join, asfrom=False, **kwargs):
        return ('(' + self.process(join.left, asfrom=True) + \
                (join.isouter and " LEFT OUTER JOIN " or " INNER JOIN ") + \
                self.process(join.right, asfrom=True) + " ON " + \
                self.process(join.onclause) + ')')

    def visit_extract(self, extract, **kw):
        field = self.extract_map.get(extract.field, extract.field)
        return 'DATEPART("%s", %s)' % \
                    (field, self.process(extract.expr, **kw))


class AccessTypeCompiler(compiler.GenericTypeCompiler):
    def visit_big_integer(self, type_, **kw):
        """
        Squeeze BigInteger() into INTEGER (a.k.a. LONG) column by default until Access ODBC supports BIGINT

        If user needs to store true BIGINT values they can convert them to string, e.g., for a pandas DataFrame:
            df = df.astype({'id': numpy.str})  # convert "id" column from int64 to string
            df.to_sql("tablename", ...)
        """
        return "INTEGER"

    def visit_text(self, type_, **kw):
        """
        The default unqualified TEXT keyword is a synonym for TEXT(255) in Access DDL.
        Use MEMO to prevent longer strings from being truncated to 255 characters.
        """
        return "MEMO"


class AccessDDLCompiler(compiler.DDLCompiler):
    def get_column_specification(self, column, **kwargs):
        if column.table is None:
            raise exc.CompileError(
                            "access requires Table-bound columns "
                            "in order to generate DDL")

        colspec = self.preparer.format_column(column)
        seq_col = column.table._autoincrement_column
        if seq_col is column:
            colspec += " AUTOINCREMENT"
        else:
            colspec += " " + self.dialect.type_compiler.process(column.type)

            if column.nullable is not None and not column.primary_key:
                if not column.nullable or column.primary_key:
                    colspec += " NOT NULL"
                else:
                    colspec += " NULL"

            default = self.get_column_default_string(column)
            if default is not None:
                colspec += " DEFAULT " + default

        return colspec

    def visit_drop_index(self, drop):
        index = drop.element
        self.append("\nDROP INDEX [%s].[%s]" % \
                        (index.table.name,
                        self._index_identifier(index.name)))


class AccessIdentifierPreparer(compiler.IdentifierPreparer):
    reserved_words = compiler.RESERVED_WORDS.copy()
    # https://support.office.com/en-us/article/learn-about-access-reserved-words-and-symbols-ae9d9ada-3255-4b12-91a9-f855bdd9c5a2
    reserved_words.update([
        'absolute', 'action', 'add', 'admindb', 'all', 'allocate', 'alphanumeric', 'alter', 'and', 'any', 'are', 'as',
        'asc', 'assertion', 'at', 'authorization', 'autoincrement', 'avg', 'band', 'begin', 'between', 'binary', 'bit',
        'bit_length', 'bnot', 'bor', 'both', 'bxor', 'by', 'byte', 'cascade', 'cascaded', 'case', 'cast', 'catalog',
        'char', 'character', 'char_length', 'character_length', 'check', 'close', 'coalesce', 'collate', 'collation',
        'column', 'commit', 'comp', 'compression', 'connect', 'connection', 'constraint', 'constraints', 'container',
        'continue', 'convert', 'corresponding', 'count', 'counter', 'create', 'createdb', 'cross', 'currency',
        'current', 'current_date', 'current_time', 'current_timestamp', 'current_user', 'cursor', 'database', 'date',
        'datetime', 'day', 'deallocate', 'dec', 'decimal', 'declare', 'default', 'deferrable', 'deferred', 'delete',
        'desc', 'describe', 'descriptor', 'diagnostics', 'disallow', 'disconnect', 'distinct', 'domain', 'double',
        'drop', 'else', 'end', 'end-exec', 'escape', 'except', 'exception', 'exclusiveconnect', 'exec', 'execute',
        'exists', 'external', 'extract', 'false', 'fetch', 'first', 'float', 'float4', 'float8', 'for', 'foreign',
        'found', 'from', 'full', 'general', 'get', 'global', 'go', 'goto', 'grant', 'group', 'guid', 'having', 'hour',
        'identity', 'ieeedouble', 'ieeesingle', 'ignore', 'image', 'immediate', 'index', 'inindex', 'indicator',
        'inheritable', 'initially', 'inner', 'input', 'insensitive', 'insert', 'int', 'integer', 'integer1',
        'integer2', 'integer4', 'intersect', 'interval', 'into', 'is', 'isolation', 'join', 'key', 'language', 'last',
        'leading', 'left', 'level', 'like', 'local', 'logical', 'logical1', 'long', 'longbinary', 'longchar',
        'longtext', 'lower', 'match', 'max', 'memo', 'min', 'minute', 'module', 'money', 'month', 'names', 'national',
        'natural', 'nchar', 'next', 'no', 'not', 'note', 'null', 'nullif', 'number', 'numeric', 'object',
        'octet_length', 'ofoleobject', 'ononly', 'open', 'option', 'ororder', 'outer', 'output', 'overlaps',
        'owneraccess', 'pad', 'parameters', 'partial', 'password', 'percent', 'pivot', 'position', 'precision',
        'prepare', 'preserve', 'primary', 'prior', 'privileges', 'proc', 'procedure', 'public', 'read', 'real',
        'references', 'relative', 'restrict', 'revoke', 'right', 'rollback', 'rows', 'schema', 'scroll', 'second',
        'section', 'select', 'selectschema', 'selectsecurity', 'session', 'session_user', 'set', 'short', 'single',
        'size', 'smallint', 'some', 'space', 'sql', 'sqlcode', 'sqlerror', 'sqlstate', 'string', 'substring', 'sum',
        'system_user', 'table', 'tableid', 'temporary', 'text', 'then', 'time', 'timestamp', 'timezone_hour',
        'timezone_minute', 'to', 'top', 'trailing', 'transaction', 'transform', 'translate', 'translation', 'trim',
        'true', 'union', 'unique', 'uniqueidentifier', 'unknown', 'update', 'updateidentity', 'updateowner',
        'updatesecurity', 'upper', 'usage', 'user', 'using', 'value', 'values', 'varbinary', 'varchar', 'varying',
        'view', 'when', 'whenever', 'where', 'with', 'work', 'write', 'year', 'yesno', 'zone',
    ])
    def __init__(self, dialect):
        super(AccessIdentifierPreparer, self).\
                __init__(dialect, initial_quote='[', final_quote=']')


class AccessDialect(default.DefaultDialect):
    colspecs = {
        types.Unicode: AcUnicode,
        types.Integer: AcInteger,
        types.SmallInteger: AcSmallInteger,
        types.Numeric: AcNumeric,
        types.Float: AcFloat,
        types.DateTime: AcDateTime,
        types.Date: AcDate,
        types.String: AcString,
        types.LargeBinary: AcBinary,
        types.Boolean: AcBoolean,
        types.Text: AcText,
        types.CHAR: AcChar,
        types.TIMESTAMP: AcTimeStamp,
    }
    name = 'access'
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False

    poolclass = pool.SingletonThreadPool
    statement_compiler = AccessCompiler
    ddl_compiler = AccessDDLCompiler
    type_compiler = AccessTypeCompiler
    preparer = AccessIdentifierPreparer
    execution_ctx_cls = AccessExecutionContext

    @classmethod
    def dbapi(cls):
        return pyodbc

    def create_connect_args(self, url):
        opts = url.translate_connect_args()
        connectors = ["Driver={Microsoft Access Driver (*.mdb)}"]
        connectors.append("Dbq=%s" % opts["database"])
        user = opts.get("username", None)
        if user:
            connectors.append("UID=%s" % user)
            connectors.append("PWD=%s" % opts.get("password", ""))
        return [[";".join(connectors)], {}]

    def last_inserted_ids(self):
        return self.context.last_inserted_ids

    def has_table(self, connection, tablename, schema=None):
        pyodbc_crsr = connection.engine.raw_connection().cursor()
        result = pyodbc_crsr.tables(table=tablename).fetchone()
        return bool(result)

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        pyodbc_crsr = connection.engine.raw_connection().cursor()
        result = pyodbc_crsr.tables(tableType='TABLE').fetchall()
        table_names = [row.table_name for row in result]
        return table_names

    def _decode_sketchy_utf16(self, raw_bytes):
        # work around bug in Access ODBC driver
        # ref: https://github.com/mkleehammer/pyodbc/issues/328
        s = raw_bytes.decode("utf-16le", "ignore")
        try:
            n = s.index('\u0000')
            s = s[:n]  # respect null terminator
        except ValueError:
            pass
        return s

    def get_columns(self, connection, table_name, schema=None, **kw):
        pyodbc_cnxn = connection.engine.raw_connection()
        # work around bug in Access ODBC driver
        # ref: https://github.com/mkleehammer/pyodbc/issues/328
        prev_converter = pyodbc_cnxn.get_output_converter(pyodbc.SQL_WVARCHAR)
        pyodbc_cnxn.add_output_converter(pyodbc.SQL_WVARCHAR, self._decode_sketchy_utf16)
        pyodbc_crsr = pyodbc_cnxn.cursor()
        result = []
        for row in pyodbc_crsr.columns(table=table_name):
            result.append({
                'name': row.column_name,
                'type': odbc_column_types[row.data_type],
                'nullable': bool(row.nullable),
                'autoincrement': (row.type_name == 'COUNTER'),
            })
        pyodbc_cnxn.add_output_converter(pyodbc.SQL_WVARCHAR, prev_converter)  # restore previous behaviour
        return result

    def get_primary_keys(self, connection, table_name, schema=None, **kw):
        return self.get_pk_constraint(self, connection, table_name, schema=schema, **kw)

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        pyodbc_crsr = connection.engine.raw_connection().cursor()
        try:
            result = pyodbc_crsr.primaryKeys(table_name)
        except pyodbc.InterfaceError as ie:
            if ie.args[0] == 'IM001':
                # ('IM001', '[IM001] [Microsoft][ODBC Driver Manager] Driver does not support this function (0) (SQLPrimaryKeys)')
                return []
            else:
                raise
        except:
            raise
        return [row[3] for row in result]

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        pyodbc_crsr = connection.engine.raw_connection().cursor()
        try:
            result = pyodbc_crsr.foreignKeys(table_name)
        except pyodbc.InterfaceError as ie:
            if ie.args[0] == 'IM001':
                # ('IM001', '[IM001] [Microsoft][ODBC Driver Manager] Driver does not support this function (0) (SQLForeignKeys)')
                return []
            else:
                raise
        except:
            raise
        # this will tell us if Access ODBC ever starts supporting SQLForeignKeys
        raise NotImplementedError()

    def get_indexes(self, connection, table_name, schema=None, **kw):
        # we might try using pyodbc's Cursor#statistics method someday, but for now ...
        return []
