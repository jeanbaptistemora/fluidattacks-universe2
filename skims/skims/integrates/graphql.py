from aiogqlc import (
    GraphQLClient,
)
from contextlib import (
    asynccontextmanager,
)
from contextvars import (
    ContextVar,
    Token,
)
from typing import (
    AsyncIterator,
)
import utils.http

# State
API_TOKEN: ContextVar[str] = ContextVar("API_TOKEN", default="")


@asynccontextmanager
async def client() -> AsyncIterator[GraphQLClient]:
    if API_TOKEN.get():
        async with utils.http.create_session(
            headers={
                "authorization": f"Bearer {API_TOKEN.get()}",
                "x-integrates-source": "skims",
            },
        ) as session:
            yield GraphQLClient(
                endpoint="https://app.fluidattacks.com/api", session=session
            )
    else:
        raise RuntimeError("create_session() must be called first")


def create_session(api_token: str) -> Token:
    return API_TOKEN.set(api_token)


def end_session(previous: Token) -> None:
    API_TOKEN.reset(previous)
