from sqlalchemy.testing.requirements import SuiteRequirements

from sqlalchemy.testing import exclusions

class Requirements(SuiteRequirements):
    @property
    def nullable_booleans(self):
        """Target database allows boolean columns to store NULL."""
        # Acccess Yes/No doesn't allow null
        return exclusions.closed()

    @property
    def temporary_tables(self):
        return exclusions.closed()

    @property
    def temporary_views(self):
        return exclusions.closed()

    @property
    def temp_table_reflection(self):
        return exclusions.closed()

    @property
    def unique_constraint_reflection(self):
        return exclusions.closed()

    @property
    def tuple_in(self):
        return exclusions.closed()
