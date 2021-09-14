from sgqlc.operation import (
    Operation,
)
from tap_announcekit.api import (
    gql_schema,
)
from tap_announcekit.api.auth import (
    get_creds,
)
from tap_announcekit.api.client import (
    ApiClient,
)
from tap_announcekit.api.gql_schema import (
    User,
)


def test_expected_project() -> None:
    client = ApiClient(get_creds())
    operation = Operation(gql_schema.Query)
    me_user = operation.me()
    me_user.active_project().name()
    print("operation: ", operation)
    data = client.endpoint(operation)
    print("raw: ", data)
    user: User = (operation + data).me
    proj_name = "[DEMO] [Staging/test] test_project"
    assert user.active_project.name == proj_name
