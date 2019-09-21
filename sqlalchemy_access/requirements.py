from sqlalchemy.testing.requirements import SuiteRequirements

from sqlalchemy.testing import exclusions


class Requirements(SuiteRequirements):
    @property
    def bound_limit_offset(self):
        return exclusions.closed()

    @property
    def foreign_key_constraint_reflection(self):
        return exclusions.closed()

    @property
    def index_reflection(self):
        return exclusions.closed()

    @property
    def nullable_booleans(self):
        """Target database allows boolean columns to store NULL."""
        # Access Yes/No doesn't allow null
        return exclusions.closed()

    @property
    def offset(self):
        # Access does LIMIT (via TOP) but not OFFSET
        return exclusions.closed()

    @property
    def parens_in_union_contained_select_w_limit_offset(self):
        return exclusions.closed()

    @property
    def primary_key_constraint_reflection(self):
        return exclusions.closed()

    @property
    def sql_expression_limit_offset(self):
        return exclusions.closed()

    @property
    def temp_table_reflection(self):
        return exclusions.closed()

    @property
    def temporary_tables(self):
        return exclusions.closed()

    @property
    def temporary_views(self):
        return exclusions.closed()

    @property
    def unique_constraint_reflection(self):
        return exclusions.closed()
