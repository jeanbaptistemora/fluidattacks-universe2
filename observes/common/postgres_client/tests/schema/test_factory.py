# Standard libraries
from typing import Any

# Third party libraries
import pytest

# Local libraries
from postgres_client import client
from postgres_client.schema import Schema


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
    db_schema = Schema.new(db_client, "test_schema")
    tables = set(db_schema.get_tables())
    assert tables == set(["table_number_one", "table_number_two"])


@pytest.mark.timeout(15, method="thread")
def test_exist_on_db(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    db_schema = Schema.new(db_client, "test_schema")
    fake_schema = Schema.new(db_client, "non_existent_schema")
    assert db_schema.exist_on_db()
    assert not fake_schema.exist_on_db()


@pytest.mark.timeout(15, method="thread")
def test_delete_on_db(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    db_schema = Schema.new(db_client, "empty_schema")
    assert db_schema.exist_on_db()
    db_schema.delete_on_db()
    assert not db_schema.exist_on_db()


@pytest.mark.timeout(15, method="thread")
def test_migrate_schema(postgresql_my: Any) -> None:
    setup_db(postgresql_my)
    db_client = client.new_test_client(postgresql_my)
    source = Schema.new(db_client, "test_schema", False)
    target = Schema.new(db_client, "target_schema", False)
    source.migrate(target)
    cursor = postgresql_my.cursor()
    assert n_rows(cursor, "target_schema", "table_number_one") == 5
    assert n_rows(cursor, "target_schema", "super_table") == 10
