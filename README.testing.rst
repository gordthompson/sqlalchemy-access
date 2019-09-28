Testing is done using pytest. After installing pytest via ``pip``, a typical run of the SQLAlchemy test suite
can be performed by running::

(venv) C:\Users\Gord\git\sqlalchemy-access>py.test

or, for more verbose output::

(venv) C:\Users\Gord\git\sqlalchemy-access>py.test -v

IMPORTANT:

1. Enable `ExtendedAnsiSQL`_ (``ExtendedAnsiSQL=1``) in your ODBC DSN.

2. Due to a limitation in Access ODBC, a couple of tests require the testing database to contain a User-defined
   System Table named ``USysSQLAlchemyDUAL``. The table must contain exactly one (1) row,
   but currently the contents of that row is irrelevant.

.. _ExtendedAnsiSQL: https://github.com/sqlalchemy/sqlalchemy-access/wiki/%5Btip%5D-use-ExtendedAnsiSQL