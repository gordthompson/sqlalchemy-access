from sqlalchemy.dialects import registry
import pytest

registry.register(
    "access.pyodbc", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc"
)

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

from sqlalchemy.testing.plugin.pytestplugin import *
