import getpass
from postgres_client import (
    connection,
)
from postgres_client.connection import (
    Credentials,
    DatabaseID,
)
from psycopg2.errors import (
    DuplicateSchema,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.timeout(15, method="thread")
@pytest.mark.xfail(getpass.getuser() == "root", reason="can not run with root")
def test_connection(
    postgresql_my: Any, get_test_creds: Credentials, get_test_db_id: DatabaseID
) -> None:
    temp_cur = postgresql_my.cursor()
    temp_cur.execute("CREATE SCHEMA test_schema")
    postgresql_my.commit()
    db_connection = connection.connect(get_test_db_id, get_test_creds)
    cursor = db_connection.get_cursor()
    with pytest.raises(DuplicateSchema):
        cursor.execute("CREATE SCHEMA test_schema")
