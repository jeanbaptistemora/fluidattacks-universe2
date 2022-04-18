# pylint: skip-file

from postgres_client import (
    client,
)
from postgres_client.schema import (
    SchemaFactory,
    SchemaID,
)
import pytest
from returns.io import (
    IO,
)
from returns.pipeline import (
    is_successful,
)
from typing import (
    Any,
)


def foo_table(
    temp_cur: Any, schema: str, table: str, records: int = 5
) -> None:
    temp_cur.execute(f"CREATE TABLE {schema}.{table} (Name VARCHAR (10))")
    for i in range(records):
        temp_cur.execute(
            f"INSERT INTO {schema}.{table} (Name) VALUES ('foo{i}')"
        )


def n_rows(temp_cur: Any, schema: str, table: str) -> int:
    temp_cur.execute(f"SELECT COUNT(*) FROM {schema}.{table}")
    return temp_cur.fetchone()[0]


def setup_db(postgresql_my: Any) -> None:
    temp_cur = postgresql_my.cursor()
    temp_cur.execute("CREATE SCHEMA test_schema")
    foo_table(temp_cur, "test_schema", "table_number_one")
    foo_table(temp_cur, "test_schema", "table_number_two")
    temp_cur.execute("CREATE SCHEMA empty_schema")
    temp_cur.execute("CREATE SCHEMA target_schema")
    foo_table(temp_cur, "target_schema", "table_number_one", 10)
    foo_table(temp_cur, "target_schema", "super_table", 10)
    postgresql_my.commit()


@pytest.mark.timeout(15, method="thread")
def test_get_tables(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    factory = SchemaFactory(db_client, False)
    db_schema_io = factory.retrieve(SchemaID("test_schema"))
    tables = db_schema_io.map(lambda schema: set(schema.get_tables()))
    assert tables == IO(set(["table_number_one", "table_number_two"]))


@pytest.mark.timeout(15, method="thread")
def test_exist_on_db(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    factory = SchemaFactory(db_client, False)
    db_schema_result = factory.try_retrieve(SchemaID("test_schema"))
    fake_schema_result = factory.try_retrieve(SchemaID("non_existent_schema"))
    assert is_successful(db_schema_result)
    assert not is_successful(fake_schema_result)


@pytest.mark.timeout(15, method="thread")
def test_delete_on_db(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    factory = SchemaFactory(db_client, False)
    db_schema_io = factory.retrieve(SchemaID("empty_schema"))
    db_schema_io.map(lambda schema: factory.delete(schema, True))
    result = factory.try_retrieve(SchemaID("empty_schema"))
    assert not is_successful(result)


@pytest.mark.timeout(15, method="thread")
def test_migrate_schema(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    factory = SchemaFactory(db_client, False)
    source = factory.retrieve(SchemaID("test_schema"))
    target = factory.retrieve(SchemaID("target_schema"))
    source.map(lambda schema: schema.migrate).bind(
        lambda migrate: target.map(migrate)
    )
    cursor = postgresql_my.cursor()
    assert n_rows(cursor, "target_schema", "table_number_one") == 5
    assert n_rows(cursor, "target_schema", "super_table") == 10


@pytest.mark.timeout(15, method="thread")
def test_rename(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    factory = SchemaFactory(db_client, False)
    db_schema_io = factory.retrieve(SchemaID("target_schema"))
    db_schema_io.map(
        lambda schema: factory.rename(schema, SchemaID("target_schema_2"))
    )
    cursor = postgresql_my.cursor()
    assert n_rows(cursor, "target_schema_2", "super_table") == 10
