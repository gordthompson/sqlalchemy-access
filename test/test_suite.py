import pytest

from sqlalchemy.testing.suite import *

from sqlalchemy.testing.suite import (
    CastTypeDecoratorTest as _CastTypeDecoratorTest,
)
from sqlalchemy.testing.suite import (
    ComponentReflectionTest as _ComponentReflectionTest,
)
from sqlalchemy.testing.suite import (
    ComponentReflectionTestExtra as _ComponentReflectionTestExtra,
)
from sqlalchemy.testing.suite import DateTimeTest as _DateTimeTest
from sqlalchemy.testing.suite import ExistsTest as _ExistsTest
from sqlalchemy.testing.suite import (
    ExpandingBoundInTest as _ExpandingBoundInTest,
)
from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest
from sqlalchemy.testing.suite import IntegerTest as _IntegerTest

try:
    from sqlalchemy.testing.suite import JoinTest as _JoinTest  # SQLA_1.4+
except ImportError:
    pass
from sqlalchemy.testing.suite import LikeFunctionsTest as _LikeFunctionsTest
from sqlalchemy.testing.suite import NumericTest as _NumericTest
from sqlalchemy.testing.suite import OrderByLabelTest as _OrderByLabelTest
from sqlalchemy.testing.suite import (
    QuotedNameArgumentTest as _QuotedNameArgumentTest,
)
from sqlalchemy.testing.suite import TableDDLTest as _TableDDLTest


class CastTypeDecoratorTest(_CastTypeDecoratorTest):
    @pytest.mark.skip()
    def test_special_type(cls):
        # Access SQL does not do CAST in the conventional way
        return


class ComponentReflectionTest(_ComponentReflectionTest):
    @pytest.mark.skip()
    def test_get_noncol_index(cls):
        # Driver does not support this function (0) (SQLPrimaryKeys)
        return

    @pytest.mark.skip()
    def test_get_unique_constraints(cls):
        # Access barfs on DDL trying to create a constraint named "i.have.dots"
        return


class ComponentReflectionTestExtra(_ComponentReflectionTestExtra):
    @pytest.mark.skip()
    def test_nullable_reflection(cls):
        # Access ODBC implementation of the SQLColumns function reports that
        # a column is nullable even when it is not
        return


class DateTimeTest(_DateTimeTest):
    @pytest.mark.skip()
    def test_null_bound_comparison(cls):
        # bypass this test because Access ODBC fails with
        # "Unrecognized keyword WHEN."
        return


class ExistsTest(_ExistsTest):
    @pytest.mark.skip()
    def test_select_exists(cls):
        # bypass this test because Access ODBC fails with
        # "SELECT statement includes a reserved word or an argument name ..."
        return

    @pytest.mark.skip()
    def test_select_exists_false(cls):
        # bypass this test because Access ODBC fails with
        # "SELECT statement includes a reserved word or an argument name ..."
        return


class ExpandingBoundInTest(_ExpandingBoundInTest):
    @pytest.mark.skip()
    def test_null_in_empty_set_is_false(cls):
        """Access SQL can't do CASE ... WHEN, but this test would pass if we
        re-wrote the query to be

            SELECT (n = 1) AS result
            FROM
                (
                    SELECT COUNT(*) AS n FROM USysSQLAlchemyDUAL
                    WHERE NULL IN (SELECT NULL FROM USysSQLAlchemyDUAL WHERE 1=0)
                )
        """
        return


class InsertBehaviorTest(_InsertBehaviorTest):
    @pytest.mark.skip()
    def test_empty_insert(cls):
        # bypass this test because Access ODBC fails with
        # [ODBC Microsoft Access Driver] Syntax error in INSERT INTO statement.
        return


class IntegerTest(_IntegerTest):
    @pytest.mark.skip()
    def test_huge_int(cls):
        # bypass this test because Access ODBC fails with
        # [ODBC Microsoft Access Driver] Optional feature not implemented.
        return


try:

    class JoinTest(_JoinTest):
        @pytest.mark.skip()
        def test_inner_join_true(cls):
            # bypass this test because Access ODBC fails with
            # "JOIN expression not supported."
            return

        @pytest.mark.skip()
        def test_inner_join_false(cls):
            # bypass this test because Access ODBC fails with
            # "JOIN expression not supported."
            return

        @pytest.mark.skip()
        def test_outer_join_false(cls):
            # bypass this test because Access ODBC fails with
            # "JOIN expression not supported."
            return


except NameError:
    pass


class LikeFunctionsTest(_LikeFunctionsTest):
    """Access SQL doesn't do ESCAPE"""

    @pytest.mark.skip()
    def test_contains_autoescape(cls):
        return

    @pytest.mark.skip()
    def test_contains_autoescape_escape(cls):
        return

    @pytest.mark.skip()
    def test_contains_escape(cls):
        return

    @pytest.mark.skip()
    def test_endswith_autoescape(cls):
        return

    @pytest.mark.skip()
    def test_endswith_autoescape_escape(cls):
        return

    @pytest.mark.skip()
    def test_endswith_escape(cls):
        return

    @pytest.mark.skip()
    def test_startswith_autoescape(cls):
        return

    @pytest.mark.skip()
    def test_startswith_autoescape_escape(cls):
        return

    @pytest.mark.skip()
    def test_startswith_escape(cls):
        return


class NumericTest(_NumericTest):
    @pytest.mark.skip()
    def test_decimal_coerce_round_trip(cls):
        # bug in Access SQL: "SELECT ? AS anon_1 ..." returns rubbish with a
        # decimal.Decimal parameter value
        # https://github.com/mkleehammer/pyodbc/issues/624
        return

    @pytest.mark.skip()
    def test_decimal_coerce_round_trip_w_cast(cls):
        # bug in Access SQL: "SELECT ? AS anon_1 ..." returns rubbish with a
        # decimal.Decimal parameter value
        # https://github.com/mkleehammer/pyodbc/issues/624
        return


class OperatorOverrideTest(fixtures.TablesTest):
    @testing.provide_metadata
    def test_not_equals_operator(self, connection):
        # test for issue #6
        tbl = Table(
            "ne_test",
            self.metadata,
            Column("id", Integer, primary_key=True),
        )
        tbl.create(connection)
        connection.execute(
            tbl.insert(),
            [{"id": 1}],
        )
        result = connection.execute(tbl.select(tbl.c.id != 1)).fetchall()
        eq_(len(result), 0)
        result = connection.execute(tbl.select(tbl.c.id != 2)).fetchall()
        eq_(len(result), 1)


class OrderByLabelTest(_OrderByLabelTest):
    @pytest.mark.skip()
    def test_composed_multiple(cls):
        # SELECT statement too complex for Access SQL
        # "Reserved error (-1001); there is no message for this error."
        return


class QuotedNameArgumentTest(_QuotedNameArgumentTest):
    @pytest.mark.skip()
    def test_get_table_options(self, name):
        return

    @pytest.mark.skip()
    def test_get_view_definition(self, name):
        return

    @pytest.mark.skip()
    def test_get_columns(self, name):
        return

    @pytest.mark.skip()
    def test_get_pk_constraint(self, name):
        return

    @pytest.mark.skip()
    def test_get_foreign_keys(self, name):
        return

    @pytest.mark.skip()
    def test_get_indexes(self, name):
        return

    @pytest.mark.skip()
    def test_get_unique_constraints(self, name):
        return

    @pytest.mark.skip()
    def test_get_table_comment(self, name):
        return

    @pytest.mark.skip()
    def test_get_check_constraints(self, name):
        return


class TableDDLTest(_TableDDLTest):
    @pytest.mark.skip()
    def test_create_table_schema(cls):
        # Access doesn't do schemas
        return

    @pytest.mark.skip()
    def test_underscore_names(cls):
        return
