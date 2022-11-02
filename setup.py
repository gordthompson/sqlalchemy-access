import os
import re

from setuptools import setup, find_packages

v = open(
    os.path.join(os.path.dirname(__file__), "sqlalchemy_access", "__init__.py")
)
VERSION = re.compile(r'.*__version__ = "(.*?)"', re.S).match(v.read()).group(1)
v.close()

readme = os.path.join(os.path.dirname(__file__), "README.rst")


setup(
    name="sqlalchemy-access",
    version=VERSION,
    description="MS Access for SQLAlchemy",
    long_description=open(readme).read(),
    url="https://github.com/gordthompson/sqlalchemy-access",
    author="Gord Thompson",
    author_email="gord@gordthompson.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database :: Front-Ends",
        "Operating System :: OS Independent",
    ],
    keywords="SQLAlchemy Microsoft Access",
    project_urls={
        "Documentation": "https://github.com/gordthompson/sqlalchemy-access/wiki",
        "Source": "https://github.com/gordthompson/sqlalchemy-access",
        "Tracker": "https://github.com/gordthompson/sqlalchemy-access/issues",
    },
    packages=find_packages(include=["sqlalchemy_access"]),
    include_package_data=True,
    install_requires=["SQLAlchemy>=2.0.0", "pyodbc>=4.0.27", "pywin32"],
    zip_safe=False,
    entry_points={
        "sqlalchemy.dialects": [
            "access.pyodbc = sqlalchemy_access.pyodbc:AccessDialect_pyodbc",
        ]
    },
)
