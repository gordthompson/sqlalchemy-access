import pyodbc
from sqlalchemy.dialects import registry

__version__ = '1.0.2'

pyodbc.pooling = False
registry.register("access.pyodbc", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc")
