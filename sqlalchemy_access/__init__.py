from sqlalchemy.dialects import registry as _registry

from .base import AcAutoNumber, AcByte, AcChar, AcCurrency, AcDateTime, AcDecimal, AcDouble, AcInteger, AcLongInteger, \
    AcLongText, AcOleObject, AcShortText, AcSingle, AcYesNo

import pyodbc

__version__ = '1.0.2'

pyodbc.pooling = False  # required for Access databases with ODBC linked tables
_registry.register("access.pyodbc", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc")
