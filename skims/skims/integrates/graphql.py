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
import os
from typing import (
    AsyncIterator,
)
from utils.env import (
    guess_environment,
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
            # Exception: WF(AsyncIterator is subtype of iterator)
            yield GraphQLClient(  # NOSONAR
                endpoint=(
                    os.environ.get("INTEGRATES_API_ENDPOINT")
                    or (
                        "https://app.fluidattacks.com/api"
                        if guess_environment() == "production"
                        else "https://127.0.0.1:8001/api"
                    )
                ),
                session=session,
            )
    else:
        raise RuntimeError("create_session() must be called first")


def create_session(api_token: str) -> Token:
    return API_TOKEN.set(api_token)


def end_session(previous: Token) -> None:
    API_TOKEN.reset(previous)
