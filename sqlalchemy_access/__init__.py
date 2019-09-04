__version__ = '1.0.0a3'

from sqlalchemy.dialects import registry

registry.register("access.pyodbc", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc")
