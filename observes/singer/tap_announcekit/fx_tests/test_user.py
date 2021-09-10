from sgqlc.endpoint.http import (
    HTTPEndpoint,
)
from sgqlc.operation import (
    Operation,
)
from tap_announcekit.api import (
    API_ENDPOINT,
    gql_schema,
)
from tap_announcekit.api.auth import (
    get_creds,
)
from tap_announcekit.api.gql_schema import (
    User,
)


def test_expected_project() -> None:
    creds = get_creds()
    endpoint = HTTPEndpoint(API_ENDPOINT, creds.basic_auth_header())
    operation = Operation(gql_schema.Query)
    me_user = operation.me()
    me_user.active_project().name()
    print("operation: ", operation)
    data = endpoint(operation)
    print("raw: ", data)
    user: User = (operation + data).me
    proj_name = "[DEMO] [Staging/test] test_project"
    assert user.active_project.name == proj_name
