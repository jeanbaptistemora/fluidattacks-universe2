from returns.io import (
    IO,
)
from tap_announcekit.api.auth import (
    get_creds,
)
from tap_announcekit.api.client import (
    ApiClient,
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.api.gql_schema import (
    User,
)
from typing import (
    cast,
)


def select_active_proj(query: Operation) -> IO[None]:
    me_user = query.me()
    me_user.active_project().name()
    return IO(None)


def test_expected_project() -> IO[None]:
    client = ApiClient(get_creds())
    query = QueryFactory.select(select_active_proj)
    user: IO[User] = client.get(query).map(lambda x: cast(User, x.me))

    def _check(user: User) -> IO[None]:
        proj_name = "[DEMO] [Staging/test] test_project"
        assert user.active_project.name == proj_name
        return IO(None)

    return user.bind(_check)
