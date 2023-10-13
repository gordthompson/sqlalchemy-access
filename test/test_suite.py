from sqlalchemy.testing.suite import *

from sqlalchemy.testing.suite import (
    BizarroCharacterFKResolutionTest as _BizarroCharacterFKResolutionTest,
)
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
from sqlalchemy.testing.suite import (
    DifficultParametersTest as _DifficultParametersTest,
)
from sqlalchemy.testing.suite import ExistsTest as _ExistsTest
from sqlalchemy.testing.suite import (
    ExpandingBoundInTest as _ExpandingBoundInTest,
)
from sqlalchemy.testing.suite import (
    FetchLimitOffsetTest as _FetchLimitOffsetTest,
)
from sqlalchemy.testing.suite import HasIndexTest as _HasIndexTest
from sqlalchemy.testing.suite import HasTableTest as _HasTableTest
from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest
from sqlalchemy.testing.suite import IntegerTest as _IntegerTest
from sqlalchemy.testing.suite import JoinTest as _JoinTest
from sqlalchemy.testing.suite import LikeFunctionsTest as _LikeFunctionsTest
from sqlalchemy.testing.suite import (
    LongNameBlowoutTest as _LongNameBlowoutTest,
)
from sqlalchemy.testing.suite import NativeUUIDTest as _NativeUUIDTest
from sqlalchemy.testing.suite import NumericTest as _NumericTest
from sqlalchemy.testing.suite import OrderByLabelTest as _OrderByLabelTest
from sqlalchemy.testing.suite import (
    QuotedNameArgumentTest as _QuotedNameArgumentTest,
)
from sqlalchemy.testing.suite import StringTest as _StringTest
from sqlalchemy.testing.suite import TableDDLTest as _TableDDLTest
from sqlalchemy.testing.suite import TrueDivTest as _TrueDivTest


class BizarroCharacterFKResolutionTest(_BizarroCharacterFKResolutionTest):
    @testing.skip("access")
    def test_fk_ref(self):
        # Access can be bizarro, but not like this
        return


class CastTypeDecoratorTest(_CastTypeDecoratorTest):
    @testing.skip("access")
    def test_special_type(self):
        # Access SQL does not do CAST in the conventional way
        return


class ComponentReflectionTest(_ComponentReflectionTest):
    @testing.skip("access")
    def test_get_foreign_keys(self):
        # Access does not support all options tested
        return

    @testing.skip("access")
    def test_get_indexes(self):
        # Access does not support all options tested
        return

    @testing.skip("access")
    def test_get_multi_columns(self):
        # tests fail due to ODBC driver bug always reporting nullable=True
        return

    @testing.skip("access")
    def test_get_multi_indexes(self):
        # tests fail because we don't support table/column comments
        return

    @testing.skip("access")
    def test_get_multi_pk_constraint(self):
        # Access does not support all options tested
        return

    @testing.skip("access")
    def test_get_multi_unique_constraints(self):
        # not implemented
        return

    @testing.skip("access")
    def test_get_noncol_index(self):
        # Access creates extra indexes that this test does not expect
        return

    @testing.skip("access")
    def test_get_pk_constraint(self):
        # PK constraint reflection (via Access.DAO) is "best effort"
        return

    @testing.skip("access")
    def test_get_unique_constraints(self):
        # Access barfs on DDL trying to create a constraint named "i.have.dots"
        return

    @testing.skip("access")
    def test_not_existing_table(self):
        return


class ComponentReflectionTestExtra(_ComponentReflectionTestExtra):
    @testing.skip("access")
    def test_nullable_reflection(self):
        # Access ODBC implementation of the SQLColumns function reports that
        # a column is nullable even when it is not
        return


class DateTimeTest(_DateTimeTest):
    @testing.skip("access")
    def test_null_bound_comparison(self):
        # bypass this test because Access ODBC fails with
        # "Unrecognized keyword WHEN."
        return


class DifficultParametersTest(_DifficultParametersTest):
    @testing.skip("access")
    def test_round_trip(self):
        # bypass this test because "q?marks" case fails with
        # "COUNT field incorrect"
        return

    @testing.skip("access")
    def test_round_trip_same_named_column(self):
        # bypass this test because CREATE TABLE statements fail for
        # "[BracketsAndCase]", "dot_s", and "q?marks" cases
        return


class ExistsTest(_ExistsTest):
    @testing.skip("access")
    def test_select_exists(self):
        # bypass this test because Access ODBC fails with
        # "SELECT statement includes a reserved word or an argument name ..."
        return

    @testing.skip("access")
    def test_select_exists_false(self):
        # bypass this test because Access ODBC fails with
        # "SELECT statement includes a reserved word or an argument name ..."
        return


class ExpandingBoundInTest(_ExpandingBoundInTest):
    @testing.skip("access")
    def test_null_in_empty_set_is_false_bindparam(self):
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

    @testing.skip("access")
    def test_null_in_empty_set_is_false_direct(self):
        return

    @testing.skip("access")
    def test_null_in_empty_set_is_false(self):
        return

    @testing.skip("access")
    def test_empty_set_against_integer_bindparam(self):
        return

    @testing.skip("access")
    def test_empty_set_against_integer_direct(self):
        return

    @testing.skip("access")
    def test_empty_set_against_string_bindparam(self):
        return

    @testing.skip("access")
    def test_empty_set_against_string_direct(self):
        return

    @testing.skip("access")
    def test_multiple_empty_sets_bindparam(self):
        return

    @testing.skip("access")
    def test_multiple_empty_sets_direct(self):
        return

    @testing.skip("access")
    def test_empty_in_plus_notempty_notin(self):
        return


class FetchLimitOffsetTest(_FetchLimitOffsetTest):
    @testing.skip("access")
    def test_limit_render_multiple_times(self):
        # bypass this test because Access ODBC fails with
        # "Query input must contain at least one table or query."
        return


class HasIndexTest(_HasIndexTest):
    @testing.skip("access")
    def test_has_index(self):
        return


class HasTableTest(_HasTableTest):
    @testing.skip("access")
    def test_has_table(self):
        return

    @testing.skip("access")
    def test_has_table_cache(self):
        return


class InsertBehaviorTest(_InsertBehaviorTest):
    @testing.skip("access")
    def test_empty_insert(self):
        # bypass this test because Access ODBC fails with
        # [ODBC Microsoft Access Driver] Syntax error in INSERT INTO statement.
        return

    @testing.skip("access")
    def test_empty_insert_multiple(self):
        # bypass this test because Access ODBC fails with
        # [ODBC Microsoft Access Driver] Syntax error in INSERT INTO statement.
        return

    @testing.skip("access")
    def test_no_results_for_non_returning_insert(self):
        return


class IntegerTest(_IntegerTest):
    @testing.skip("access")
    def test_huge_int(self):
        # bypass this test because Access ODBC fails with
        # [ODBC Microsoft Access Driver] Optional feature not implemented.
        return

    @testing.skip("access")
    def test_huge_int_auto_accommodation(self):
        return


class JoinTest(_JoinTest):
    @testing.skip("access")
    def test_inner_join_true(self):
        # bypass this test because Access ODBC fails with
        # "JOIN expression not supported."
        return

    @testing.skip("access")
    def test_inner_join_false(self):
        # bypass this test because Access ODBC fails with
        # "JOIN expression not supported."
        return

    @testing.skip("access")
    def test_outer_join_false(self):
        # bypass this test because Access ODBC fails with
        # "JOIN expression not supported."
        return


class LikeFunctionsTest(_LikeFunctionsTest):
    """Access SQL doesn't do ESCAPE"""

    @testing.skip("access")
    def test_contains_autoescape(self):
        return

    @testing.skip("access")
    def test_contains_autoescape_escape(self):
        return

    @testing.skip("access")
    def test_contains_escape(self):
        return

    @testing.skip("access")
    def test_contains_unescaped(self):
        return

    @testing.skip("access")
    def test_endswith_autoescape(self):
        return

    @testing.skip("access")
    def test_endswith_autoescape_escape(self):
        return

    @testing.skip("access")
    def test_endswith_escape(self):
        return

    @testing.skip("access")
    def test_startswith_autoescape(self):
        return

    @testing.skip("access")
    def test_startswith_autoescape_escape(self):
        return

    @testing.skip("access")
    def test_startswith_escape(self):
        return


class LongNameBlowoutTest(_LongNameBlowoutTest):
    @testing.skip("access")
    def test_long_convention_name(self):
        # test generates names that are *way* too long for Access
        return


class NativeUUIDTest(_NativeUUIDTest):
    @testing.skip("access")
    def test_literal_text(self):
        return

    @testing.skip("access")
    def test_literal_uuid(self):
        return

    @testing.skip("access")
    def test_uuid_round_trip(self):
        return

    @testing.skip("access")
    def test_uuid_text_round_trip(self):
        return


class NumericTest(_NumericTest):
    @testing.skip("access")
    def test_decimal_coerce_round_trip(self):
        # bug in Access SQL: "SELECT ? AS anon_1 ..." returns rubbish with a
        # decimal.Decimal parameter value
        # https://github.com/mkleehammer/pyodbc/issues/624
        return

    @testing.skip("access")
    def test_decimal_coerce_round_trip_w_cast(self):
        # bug in Access SQL: "SELECT ? AS anon_1 ..." returns rubbish with a
        # decimal.Decimal parameter value
        # https://github.com/mkleehammer/pyodbc/issues/624
        return

    @testing.skip("access")
    def test_float_is_not_numeric(self):
        # test fails because: 'numeric' != 'numeric'
        # (umm, okay …)
        return


class OrderByLabelTest(_OrderByLabelTest):
    @testing.skip("access")
    def test_composed_multiple(self):
        # SELECT statement too complex for Access SQL
        # "Reserved error (-1001); there is no message for this error."
        return


class QuotedNameArgumentTest(_QuotedNameArgumentTest):
    # suppress creation of test table(s) since that's where the errors occur
    run_create_tables = None

    @testing.skip("access")
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_table_options(self, name):
        return

    @testing.skip("access")
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_view_definition(self, name):
        return

    @testing.skip("access")
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_columns(self, name):
        return

    @testing.skip("access")
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_pk_constraint(self, name):
        return

    @testing.skip("access")
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_foreign_keys(self, name):
        return

    @testing.skip("access")
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_indexes(self, name):
        return

    @testing.skip("access")
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_unique_constraints(self, name):
        return

    @testing.skip("access")
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_table_comment(self, name):
        return

    @testing.skip("access")
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_check_constraints(self, name):
        return


class StringTest(_StringTest):
    @testing.skip("access")
    def test_concatenate_clauselist(self):
        return


class TableDDLTest(_TableDDLTest):
    @testing.skip("access")
    def test_underscore_names(self):
        return


class TrueDivTest(_TrueDivTest):
    @testing.skip("access")
    def test_floordiv_integer(self):
        return

    @testing.skip("access")
    def test_floordiv_integer_bound(self):
        return

    @testing.skip("access")
    def test_floordiv_numeric(self):
        return

    @testing.skip("access")
    def test_truediv_numeric(self):
        return
