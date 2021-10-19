"""Fluid Forces Integrates api client."""

from aiogqlc import (
    GraphQLClient,
)
import aiohttp
from aiohttp.client_exceptions import (
    ClientResponseError,
)
import contextlib
from contextvars import (
    ContextVar,
    Token,
)
from forces.apis.integrates import (
    get_api_token,
)
from forces.utils.logs import (
    blocking_log,
)
from typing import (
    Any,
    AsyncIterator,
    Dict,
    List,
    Optional,
    TypeVar,
)

# Context
SESSION: ContextVar[GraphQLClient] = ContextVar("SESSION")
TVar = TypeVar("TVar")


class ApiError(Exception):
    def __init__(self, *errors: Dict[str, Any]) -> None:
        self.messages: List[str] = []
        for error in errors:
            if message := error.get("message"):
                self.messages.append(message)
                blocking_log("error", message)
        super().__init__(*errors)


@contextlib.asynccontextmanager
async def session(
    api_token: str = "",
    endpoint_url: str = "https://app.fluidattacks.com/api",
    **kwargs: str,
) -> AsyncIterator[GraphQLClient]:
    """Returns an Async GraphQL Client."""
    try:
        yield SESSION.get()
    except LookupError:
        api_token = api_token or get_api_token()
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                verify_ssl=False,
            ),
            headers={
                "authorization": f"Bearer {api_token}",
                **kwargs,
            },
        ) as client_session:
            client = GraphQLClient(endpoint_url, session=client_session)
            token: Token[Any] = SESSION.set(client)
            try:
                yield SESSION.get()
            finally:
                SESSION.reset(token)


async def execute(
    query: str,
    operation_name: str,
    variables: Optional[Dict[str, Any]] = None,
    default: Optional[Any] = None,
    **kwargs: Any,
) -> TVar:
    async with session(**kwargs) as client:
        result: Any
        response: aiohttp.ClientResponse

        response = await client.execute(
            query,
            variables=variables,
            operation=operation_name,
        )

        try:
            result = await response.json()
        except ClientResponseError:
            raise ApiError(
                dict(
                    status=getattr(response, "status", "unknown"),
                    reason=getattr(response, "reason", "unknown"),
                    ok=getattr(response, "ok", False),
                )
            )
        if "errors" in result.keys():
            raise ApiError(*result["errors"])

        result = result.get("data", {})
        return result or default  # type: ignore
