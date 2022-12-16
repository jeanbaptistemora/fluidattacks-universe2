from contextlib import (
    contextmanager,
)
from gql.client import (
    Client as GraphQLClient,
)
from gql.transport.requests import (
    RequestsHTTPTransport,
)
from gql.transport.transport import (
    Transport,
)
from sorts.constants import (
    CTX,
)
from typing import (
    Iterator,
)


@contextmanager
def client() -> Iterator[GraphQLClient]:
    if hasattr(CTX, "api_token") and CTX.api_token:
        transport: Transport = RequestsHTTPTransport(
            headers={"Authorization": f"Bearer {CTX.api_token}"},
            timeout=20,
            url="https://app.fluidattacks.com/api",
        )
        yield GraphQLClient(
            transport=transport,
            fetch_schema_from_transport=True,
        )
    else:
        raise RuntimeError("create_session() must be called first")


def create_session(api_token: str) -> str:
    CTX.api_token = api_token
    return CTX.api_token


def end_session(previous: str) -> None:
    CTX.api_token = previous
