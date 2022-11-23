from postgres_client.connection import (
    Credentials,
    DatabaseID,
)
import pytest
from pytest_postgresql import (
    factories,
)
import random
import string


def _rand_str(num: int) -> str:
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=num)
    )


test_creds = Credentials(user=_rand_str(10), password=_rand_str(15))
test_db_id = DatabaseID(db_name="TheSuperDB", host="127.0.0.1", port=44565)

postgresql_my_proc = factories.postgresql_proc(
    host=test_db_id.host,
    port=test_db_id.port,
    user=test_creds.user,
    password=test_creds.password,
    unixsocketdir=".",
)
postgresql_my = factories.postgresql(
    "postgresql_my_proc", db_name=test_db_id.db_name
)


@pytest.fixture(scope="function")
def get_test_creds() -> Credentials:
    return test_creds


@pytest.fixture(scope="function")
def get_test_db_id() -> DatabaseID:
    return test_db_id
