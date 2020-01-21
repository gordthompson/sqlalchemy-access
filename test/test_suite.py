from sqlalchemy.testing.suite import *

from sqlalchemy.testing.suite import (
    ComponentReflectionTest as _ComponentReflectionTest,
)
from sqlalchemy.testing.suite import DateTimeTest as _DateTimeTest
from sqlalchemy.testing.suite import (
    ExpandingBoundInTest as _ExpandingBoundInTest,
)
from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest
from sqlalchemy.testing.suite import IntegerTest as _IntegerTest
from sqlalchemy.testing.suite import JoinTest as _JoinTest
from sqlalchemy.testing.suite import LikeFunctionsTest as _LikeFunctionsTest
from sqlalchemy.testing.suite import NumericTest as _NumericTest
from sqlalchemy.testing.suite import OrderByLabelTest as _OrderByLabelTest
from sqlalchemy.testing.suite import TableDDLTest as _TableDDLTest


class ComponentReflectionTest(_ComponentReflectionTest):
    @classmethod
    def test_get_noncol_index_pk(cls):
        # This test fails because Access automatically creates a unique
        # *index* (not constraint) on the primary key. The test is expecting
        # to see just one index (on a non-PK column) but it is seeing two.
        return

    @classmethod
    def test_get_unique_constraints(cls):
        # Access barfs on DDL trying to create a constraint named "i.have.dots"
        return

    @classmethod
    def test_nullable_reflection(cls):
        # Access ODBC implementation of the SQLColumns function reports that
        # a column is nullable even when it is not
        return


class DateTimeTest(_DateTimeTest):
    @classmethod
    def test_null_bound_comparison(cls):
        # bypass this test because Access ODBC fails with
        # "Unrecognized keyword WHEN."
        return


class ExpandingBoundInTest(_ExpandingBoundInTest):
    @classmethod
    def test_null_in_empty_set_is_false(cls):
        """ Access SQL can't do CASE ... WHEN, but this test would pass if we
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
    @classmethod
    def test_empty_insert(cls):
        # bypass this test because Access ODBC fails with
        # [ODBC Microsoft Access Driver] Syntax error in INSERT INTO statement.
        return


class IntegerTest(_IntegerTest):
    @classmethod
    def test_huge_int(cls):
        # bypass this test because Access ODBC fails with
        # [ODBC Microsoft Access Driver] Optional feature not implemented.
        return


class JoinTest(_JoinTest):
    @classmethod
    def test_inner_join_true(cls):
        # bypass this test because Access ODBC fails with
        # "JOIN expression not supported."
        return

    @classmethod
    def test_inner_join_false(cls):
        # bypass this test because Access ODBC fails with
        # "JOIN expression not supported."
        return

    @classmethod
    def test_outer_join_false(cls):
        # bypass this test because Access ODBC fails with
        # "JOIN expression not supported."
        return


class LikeFunctionsTest(_LikeFunctionsTest):
    # Access SQL doesn't do ESCAPE
    @classmethod
    def test_contains_autoescape(cls):
        return

    @classmethod
    def test_contains_autoescape_escape(cls):
        return

    @classmethod
    def test_contains_escape(cls):
        return

    @classmethod
    def test_endswith_autoescape(cls):
        return

    @classmethod
    def test_endswith_autoescape_escape(cls):
        return

    @classmethod
    def test_endswith_escape(cls):
        return

    @classmethod
    def test_startswith_autoescape(cls):
        return

    @classmethod
    def test_startswith_autoescape_escape(cls):
        return

    @classmethod
    def test_startswith_escape(cls):
        return


class NumericTest(_NumericTest):
    @classmethod
    def test_decimal_coerce_round_trip(cls):
        # bug in Access SQL: "SELECT ? AS anon_1 ..." returns rubbish with a
        # decimal.Decimal parameter value
        # https://github.com/mkleehammer/pyodbc/issues/624
        return

    @classmethod
    def test_decimal_coerce_round_trip_w_cast(cls):
        # bug in Access SQL: "SELECT ? AS anon_1 ..." returns rubbish with a
        # decimal.Decimal parameter value
        # https://github.com/mkleehammer/pyodbc/issues/624
        return


class OrderByLabelTest(_OrderByLabelTest):
    @classmethod
    def test_composed_multiple(cls):
        # SELECT statement too complex for Access SQL
        # "Reserved error (-1001); there is no message for this error."
        return


class TableDDLTest(_TableDDLTest):
    # Access doesn't do schemas
    @classmethod
    def test_create_table_schema(cls):
        return

    @classmethod
    def test_underscore_names(cls):
        return
