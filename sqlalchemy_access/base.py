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
        return "TEXT" + (self.length and ("(%d)" % self.length) or "")

class AcUnicode(types.Unicode):
    def get_col_spec(self):
        return "TEXT" + (self.length and ("(%d)" % self.length) or "")

    def bind_processor(self, dialect):
        return None

    def result_processor(self, dialect, coltype):
        return None

class AcChar(types.CHAR):
    def get_col_spec(self):
        return "TEXT" + (self.length and ("(%d)" % self.length) or "")

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

    def visit_select_precolumns(self, select):
        """Access puts TOP, it's version of LIMIT here """
        s = select.distinct and "DISTINCT " or ""
        if select.limit:
            s += "TOP %s " % (select.limit)
        if select.offset:
            raise exc.InvalidRequestError(
                    'Access does not support LIMIT with an offset')
        return s

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
    def visit_function(self, func):
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
    reserved_words.update(['value', 'text'])
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
    preparer = AccessIdentifierPreparer
    execution_ctx_cls = AccessExecutionContext

    @classmethod
    def dbapi(cls):
        import pyodbc as module
        return module

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
        result = connection.scalar(
                        sql.text(
                            "select count(*) from msysobjects where "
                            "type=1 and name=:name"), name=tablename
                        )
        return bool(result)

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        result = connection.execute("select name from msysobjects where "
                "type=1 and name not like 'MSys%'")
        table_names = [r[0] for r in result]
        return table_names


