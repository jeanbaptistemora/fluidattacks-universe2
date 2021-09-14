from returns.io import (
    IO,
)
from tap_announcekit.api.auth import (
    get_creds,
)
from tap_announcekit.api.client import (
    ApiClient,
    Query,
)
from tap_announcekit.api.gql_schema import (
    User,
)


def _select_active_proj(query: Query) -> IO[None]:
    me_user = query.raw.me()
    me_user.active_project().name()
    return IO(None)


def test_expected_project() -> IO[None]:
    client = ApiClient(get_creds())
    query = ApiClient.new_query()
    query.bind(_select_active_proj)
    user: IO[User] = client.get(query).map(lambda x: x.me)

    def _check(user: User) -> None:
        proj_name = "[DEMO] [Staging/test] test_project"
        assert user.active_project.name == proj_name

    user.bind(_check)
