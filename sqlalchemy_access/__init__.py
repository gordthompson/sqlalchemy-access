from sqlalchemy.dialects import registry as _registry

from .base import (
    AutoNumber,
    Byte,
    Char,
    Currency,
    DateTime,
    Decimal,
    Double,
    Integer,
    LongInteger,
    LongText,
    OleObject,
    ReplicationID,
    ShortText,
    Single,
    YesNo,
)

import pyodbc

__version__ = "1.0.6"

pyodbc.pooling = False  # required for Access databases with ODBC linked tables
_registry.register(
    "access.pyodbc", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc"
)
