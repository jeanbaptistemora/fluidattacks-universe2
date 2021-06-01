from postgres_client import (
    client,
    table,
)
from postgres_client.table import (
    DbTable,
    operations,
    TableID,
)
import pytest
from returns.pipeline import (
    is_successful,
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
    old_table = TableID(schema="test_schema", table_name="table_number_one")
    new_table_id = operations.rename(db_client, old_table, "renamed_table")
    assert not is_successful(table.exist(db_client, old_table))
    assert is_successful(table.exist(db_client, new_table_id))


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
