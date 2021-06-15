from aioextensions import (
    rate_limited,
)
from aiohttp import (
    ClientError,
    ClientSession,
)
import logging
from typing import (
    Any,
    Awaitable,
    Callable,
    cast,
    Coroutine,
    Dict,
    List,
    NamedTuple,
    Optional,
)
import urllib.parse

LOG = logging.getLogger(__name__)


class GitlabResource(NamedTuple):
    project: str
    resource: str
    params: frozenset = frozenset()


class GitlabResourcePage(NamedTuple):
    g_resource: GitlabResource
    page: int
    per_page: int


class GResourcePageRange(NamedTuple):
    g_resource: GitlabResource
    page_range: range
    per_page: int


class MaxRetriesReached(Exception):
    def __init__(self, msg: str):
        LOG.error("Max retries reached: %s", msg)
        super().__init__(msg)


@rate_limited(
    # Gitlab allows at most 10 per second, not bursted
    max_calls=5,
    max_calls_period=1,
    min_seconds_between_calls=0.2,
)
async def get_json(
    session: ClientSession, endpoint: str, **kargs: Any
) -> List[Dict[str, Any]]:
    """Get as JSON the result of a GET request to endpoint."""
    async with session.get(endpoint, **kargs) as response:
        LOG.debug("[%s]", response.status)
        LOG.debug("\tEndpoint: %s", endpoint)
        LOG.debug("\tParams: %s", kargs["params"])
        LOG.debug("\tHeaders: %s", kargs["headers"].keys())
        response.raise_for_status()

        return await response.json()


async def get_json_less_than(
    target_id: int, session: ClientSession, endpoint: str, **kargs: Any
) -> List[Dict[str, Any]]:
    """Filter `get_json` result using `elements_less_than` filter"""
    raw_data = await get_json(session, endpoint, **kargs)
    return elements_less_than(target_id, raw_data)


def elements_less_than(
    target_id: int, data: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Returns data where elements id are less than `target_id`"""
    result: List[Dict[str, Any]] = []
    for item in data:
        if item["id"] < target_id:
            result.append(item)
    return result


def elements_greater_than(
    target_id: int, data: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Returns data where elements id are greater than `target_id`"""
    result: List[Dict[str, Any]] = []
    for item in data:
        if item["id"] > target_id:
            result.append(item)
    return result


def get_minor_id(data: List[Dict[str, Any]]) -> Optional[int]:
    if data:
        LOG.debug("minor id: %s", int(data[-1]["id"]))
        return int(data[-1]["id"])
    return None


def build_getter(
    less_than: Optional[int],
) -> Callable[..., Coroutine[Any, Any, List[Dict[str, Any]]]]:
    if less_than is not None:

        async def filtered_getter(
            session: ClientSession, endpoint: str, **kargs: Any
        ) -> List[Dict[str, Any]]:
            getter = insistent_endpoint_call(get_json_less_than)
            return await getter(
                cast(int, less_than), session, endpoint, **kargs
            )

        return filtered_getter

    async def normal_getter(
        session: ClientSession, endpoint: str, **kargs: Any
    ) -> List[Dict[str, Any]]:
        getter = insistent_endpoint_call(get_json, 100)
        return await getter(session, endpoint, **kargs)

    return normal_getter


def insistent_endpoint_call(
    get_request: Callable[..., Awaitable],
    max_errors: int = 10,
) -> Callable[..., Awaitable]:
    async def i_getter(*args: Any, **kargs: Any) -> Any:
        errors: int = 0
        while errors <= max_errors:
            try:
                result = await get_request(*args, **kargs)
                return result
            except ClientError as exc:
                errors += 1
                LOG.error("h_error # %s: %s", errors, type(exc).__name__)
        if errors >= max_errors:
            raise MaxRetriesReached(
                f"#{errors} ClientErrors",
            )

    return i_getter


async def get_resource(
    session: ClientSession,
    resource: GitlabResourcePage,
    less_than: Optional[int] = None,
    **kargs: Any,
) -> List[Dict[str, Any]]:
    endpoint = (
        "https://gitlab.com/api/v4/projects/"
        + urllib.parse.quote(f"{resource.g_resource.project}", safe="")
        + f"/{resource.g_resource.resource}"
    )
    params = {"page": resource.page, "per_page": resource.per_page}
    params.update(dict(resource.g_resource.params))
    get_data = build_getter(less_than)
    return await get_data(session, endpoint, params=params, **kargs)
