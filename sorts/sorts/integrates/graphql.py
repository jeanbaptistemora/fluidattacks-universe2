# Standard libraries
from contextlib import contextmanager
from typing import Iterator

# Third party libraries
from gql.client import Client as GraphQLClient
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.transport import Transport

# Local libraries
from sorts.constants import CTX


@contextmanager
def client() -> Iterator[GraphQLClient]:
    if hasattr(CTX, 'api_token') and CTX.api_token:
        transport: Transport = RequestsHTTPTransport(
            headers={'Authorization': f'Bearer {CTX.api_token}'},
            timeout=5,
            url='https://app.fluidattacks.com/api'
        )
        yield GraphQLClient(transport=transport)
    else:
        raise RuntimeError('create_session() must be called first')


def create_session(api_token: str) -> str:
    CTX.api_token = api_token
    return CTX.api_token


def end_session(previous: str) -> None:
    CTX.api_token = previous
