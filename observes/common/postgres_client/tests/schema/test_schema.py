# Standard libraries
from typing import Any
# Third party libraries
import pytest
# Local libraries
from postgres_client import client
from postgres_client.schema import factory


@pytest.mark.timeout(15, method='thread')
def test_get_tables(postgresql_my: Any) -> None:
    temp_cur = postgresql_my.cursor()
    temp_cur.execute('CREATE SCHEMA test_schema')
    temp_cur.execute(
        'CREATE TABLE test_schema.table_number_one '
        '(Name CHARACTER (30))'
    )
    temp_cur.execute(
        'CREATE TABLE test_schema.table_number_two'
        '(Name CHARACTER (30))'
    )
    postgresql_my.commit()
    db_client = client.new_test_client(postgresql_my)
    db_schema = factory.db_schema(db_client, 'test_schema')
    tables = set(db_schema.get_tables())
    assert tables == set(['table_number_one', 'table_number_two'])
