# Standard libraries
from contextvars import Token
from contextlib import contextmanager
from typing import Iterator

# Third party libraries
from gql.client import Client as GraphQLClient
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.transport import Transport

# Local libraries
from sorts.constants import API_TOKEN


@contextmanager
def client() -> Iterator[GraphQLClient]:
    if API_TOKEN.get():
        transport: Transport = RequestsHTTPTransport(
            headers={'Authorization': f'Bearer {API_TOKEN.get()}'},
            timeout=5,
            url='https://app.fluidattacks.com/api'
        )
        yield GraphQLClient(transport=transport)
    else:
        raise RuntimeError('create_session() must be called first')


def create_session(api_token: str) -> Token:
    return API_TOKEN.set(api_token)


def end_session(previous: Token) -> None:
    API_TOKEN.reset(previous)
