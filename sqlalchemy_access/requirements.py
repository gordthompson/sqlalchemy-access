from sqlalchemy.testing.requirements import SuiteRequirements

from sqlalchemy.testing import exclusions

class Requirements(SuiteRequirements):
    @property
    def nullable_booleans(self):
        """Target database allows boolean columns to store NULL."""
        # Acccess Yes/No doesn't allow null
        return exclusions.closed()
