from sqlalchemy.testing.suite import *


from sqlalchemy.testing.suite import ComponentReflectionTest as _ComponentReflectionTest

class ComponentReflectionTest(_ComponentReflectionTest):
    @classmethod
    def define_views(cls, metadata, schema):
        return
        for table_name in ('users', 'email_addresses'):
            fullname = table_name
            if schema:
                fullname = "%s.%s" % (schema, table_name)
            view_name = fullname + '_v'
            query = "CREATE VIEW %s AS SELECT * FROM %s" % (
                                view_name, fullname)
            event.listen(
                metadata,
                "after_create",
                DDL(query)
            )
            event.listen(
                metadata,
                "before_drop",
                DDL("DROP VIEW %s" % view_name)
            )
