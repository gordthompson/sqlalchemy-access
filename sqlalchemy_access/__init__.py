__version__ = '1.0.0a1'

from sqlalchemy.dialects import registry

registry.register("access", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc")
registry.register("access.pyodbc", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc")
