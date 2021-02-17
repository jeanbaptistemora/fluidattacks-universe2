# Standard libraries
from typing import Any
# Third party libraries
import pytest
# Local libraries
from postgres_client import client
from postgres_client import table
from postgres_client.table import (
    operations,
    TableID
)


@pytest.mark.timeout(15, method='thread')
def test_schema_get_tables(postgresql_my: Any) -> None:
    temp_cur = postgresql_my.cursor()
    temp_cur.execute('CREATE SCHEMA test_schema')
    temp_cur.execute(
        'CREATE TABLE test_schema.table_number_one '
        '(Name CHARACTER (30))'
    )
    postgresql_my.commit()
    db_client = client.new_test_client(postgresql_my)
    old_table = TableID(schema='test_schema', table_name='table_number_one')
    new_table_id = operations.rename(db_client, old_table, 'renamed_table')
    assert not table.exist(db_client, old_table)
    assert table.exist(db_client, new_table_id)
