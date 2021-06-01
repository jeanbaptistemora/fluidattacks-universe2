from postgres_client import (
    client,
)
from postgres_client.table import (
    DbTable,
    TableID,
)
import pytest
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Any,
)


def setup_db(postgresql_my: Any) -> None:
    temp_cur = postgresql_my.cursor()
    temp_cur.execute("CREATE SCHEMA test_schema")
    temp_cur.execute("CREATE SCHEMA test_schema_2")
    temp_cur.execute(
        "CREATE TABLE test_schema.table_number_one " "(Name CHARACTER (30))"
    )
    postgresql_my.commit()


@pytest.mark.timeout(15, method="thread")
def test_create_like(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    blueprint_id = TableID(schema="test_schema", table_name="table_number_one")
    new_table_id = TableID(schema="test_schema_2", table_name="the_table")
    blueprint_io = DbTable.retrieve(db_client.cursor, blueprint_id, False)
    new_table_io = DbTable.create_like(
        db_client.cursor, blueprint_id, new_table_id, False
    )
    blueprint = unsafe_perform_io(blueprint_io)
    new_table = unsafe_perform_io(new_table_io)
    assert new_table.table.table_id != blueprint.table.table_id
    assert new_table.table.columns == blueprint.table.columns
    assert new_table.table.primary_keys == blueprint.table.primary_keys
