from postgres_client import (
    client,
    table,
)
from postgres_client.table import (
    DbTable,
    TableID,
)
import pytest
from returns.pipeline import (
    is_successful,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Any,
)


def setup_db(postgresql_my: Any) -> None:
    temp_cur = postgresql_my.cursor()
    temp_cur.execute("CREATE SCHEMA test_schema")
    temp_cur.execute(
        "CREATE TABLE test_schema.table_number_one " "(Name VARCHAR (30))"
    )
    temp_cur.execute(
        "INSERT INTO test_schema.table_number_one (Name) "
        "VALUES ('Juan Lopez');"
    )
    postgresql_my.commit()


@pytest.mark.timeout(15, method="thread")
def test_rename(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    old_table_id = TableID(schema="test_schema", table_name="table_number_one")
    old_table = unsafe_perform_io(
        DbTable.retrieve(db_client.cursor, old_table_id, False)
    )
    new_table_id = unsafe_perform_io(old_table.rename("renamed_table"))
    new_table = unsafe_perform_io(
        DbTable.retrieve(db_client.cursor, new_table_id, False)
    )
    assert not is_successful(table.exist(db_client, old_table_id))
    assert new_table.table.table_id == new_table_id


@pytest.mark.timeout(15, method="thread")
def test_delete(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    target = TableID(schema="test_schema", table_name="table_number_one")
    table_io = DbTable.retrieve(db_client.cursor, target)
    table_io.map(lambda table: table.delete())
    assert not is_successful(table.exist(db_client, target))


@pytest.mark.skip(
    reason=(
        "move procedure uses specific redshift statement "
        "not supported on test db"
    )
)
def test_move() -> None:
    pass
