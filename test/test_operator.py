from sqlalchemy import testing, Table, Column, Integer
from sqlalchemy.testing import fixtures, eq_


class OperatorOverrideTest(fixtures.TablesTest):
    @testing.provide_metadata
    def test_not_equals_operator(self, connection):
        # test for issue #6
        tbl = Table(
            "ne_test",
            self.metadata,
            Column("id", Integer, primary_key=True),
        )
        tbl.create(connection)
        connection.execute(
            tbl.insert(),
            [{"id": 1}],
        )
        result = connection.execute(tbl.select().where(tbl.c.id != 1)).fetchall()
        eq_(len(result), 0)
        result = connection.execute(tbl.select().where(tbl.c.id != 2)).fetchall()
        eq_(len(result), 1)
