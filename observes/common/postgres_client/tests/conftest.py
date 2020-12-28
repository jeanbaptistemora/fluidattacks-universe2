# Standard libraries
# Third party libraries
import pytest
from pytest_postgresql import factories
# Local libraries
from postgres_client.connection import (
    Credentials, DatabaseID
)


test_creds = Credentials(user='Light_Yagami', password='EtOn_HtAeD')
test_db_id = DatabaseID(
    db_name='TheSuperDB',
    host='127.0.0.1',
    port=44565
)

postgresql_my_proc = factories.postgresql_proc(
    host=test_db_id.host, port=test_db_id.port,
    user=test_creds.user, password=test_creds.password,
    unixsocketdir='/var/run/postgresql')
postgresql_my = factories.postgresql(
    'postgresql_my_proc', db_name=test_db_id.db_name
)


@pytest.fixture(scope='function')  # type: ignore
def get_test_creds() -> Credentials:
    return test_creds


@pytest.fixture(scope='function')  # type: ignore
def get_test_db_id() -> DatabaseID:
    return test_db_id
