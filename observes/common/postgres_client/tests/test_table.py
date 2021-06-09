from postgres_client import (
    client,
)
from postgres_client.column import (
    ColumnType,
    RedshiftDataType,
)
from postgres_client.schema import (
    SchemaID,
)
from postgres_client.table import (
    Column,
    MetaTable,
    TableFactory,
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
        "CREATE TABLE test_schema.table_number_one (Name VARCHAR (30))"
    )
    temp_cur.execute(
        "INSERT INTO test_schema.table_number_one (Name) "
        "VALUES ('Juan Lopez');"
    )
    temp_cur.execute("CREATE SCHEMA test_schema_2")
    postgresql_my.commit()


@pytest.mark.timeout(15, method="thread")
def test_create(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    schema = SchemaID("test_schema")
    factory = TableFactory(db_client.cursor, False)
    table_id = TableID(schema, "super_table_N1")
    columns = [
        Column("id", ColumnType(RedshiftDataType.VARCHAR)),
        Column("some_char", ColumnType(RedshiftDataType.CHAR)),
        Column("some_sint", ColumnType(RedshiftDataType.SMALLINT)),
        Column("some_real", ColumnType(RedshiftDataType.REAL)),
        Column("some_bool", ColumnType(RedshiftDataType.BOOLEAN)),
        Column("some_tstamp", ColumnType(RedshiftDataType.TIMESTAMP)),
    ]
    draft = MetaTable.new(
        table_id,
        frozenset(["id"]),
        frozenset(columns),
    )
    table1 = unsafe_perform_io(factory.new_table(draft))
    table2 = unsafe_perform_io(factory.retrieve(table_id))
    assert table1.table.columns == table2.table.columns


@pytest.mark.timeout(15, method="thread")
def test_create_like(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    blueprint_id = TableID(
        schema=SchemaID("test_schema"), table_name="table_number_one"
    )
    new_table_id = TableID(
        schema=SchemaID("test_schema_2"), table_name="the_table"
    )
    factory = TableFactory(db_client.cursor, False)
    blueprint_io = factory.retrieve(blueprint_id)
    new_table_io = factory.create_like(blueprint_id, new_table_id)
    blueprint = unsafe_perform_io(blueprint_io)
    new_table = unsafe_perform_io(new_table_io)
    assert new_table.table.table_id != blueprint.table.table_id
    assert new_table.table.columns == blueprint.table.columns
    assert new_table.table.primary_keys == blueprint.table.primary_keys


@pytest.mark.timeout(15, method="thread")
def test_rename(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    old_table_id = TableID(
        schema=SchemaID("test_schema"), table_name="table_number_one"
    )
    factory = TableFactory(db_client.cursor, False)
    old_table = unsafe_perform_io(factory.retrieve(old_table_id))
    new_table_id = unsafe_perform_io(old_table.rename("renamed_table"))
    new_table = unsafe_perform_io(factory.retrieve(new_table_id))
    assert not is_successful(factory.exist(old_table_id))
    assert new_table.table.table_id == new_table_id


@pytest.mark.timeout(15, method="thread")
def test_delete(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    target = TableID(
        schema=SchemaID("test_schema"), table_name="table_number_one"
    )
    factory = TableFactory(db_client.cursor, False)
    table_io = factory.retrieve(target)
    table_io.map(lambda table: table.delete())
    assert not is_successful(factory.exist(target))


@pytest.mark.skip(
    reason=(
        "move procedure uses specific redshift statement "
        "not supported on test db"
    )
)
def test_move() -> None:
    # non testable
    pass
