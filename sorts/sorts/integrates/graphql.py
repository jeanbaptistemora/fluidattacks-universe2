# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
            timeout=10,
            url="https://app.fluidattacks.com/api",
            retries=3,
        )
        yield GraphQLClient(transport=transport)
    else:
        raise RuntimeError("create_session() must be called first")


def create_session(api_token: str) -> str:
    CTX.api_token = api_token
    return CTX.api_token


def end_session(previous: str) -> None:
    CTX.api_token = previous
