# Standard libraries
from typing import (
    Any,
    Callable,
    Coroutine,
    cast,
    Dict,
    Optional,
    List,
    NamedTuple,
)
# Third party libraries
from aiohttp import (
    ClientSession,
)
from aioextensions import (
    rate_limited,
)
# Local libraries
from streamer_gitlab.log import log


class GitlabResource(NamedTuple):
    project: str
    resource: str


class GitlabResourcePage(NamedTuple):
    g_resource: GitlabResource
    page: int
    per_page: int


class GResourcePageRange(NamedTuple):
    g_resource: GitlabResource
    page_range: range
    per_page: int


@rate_limited(
    # Gitlab allows at most 10 per second, not bursted
    max_calls=5,
    max_calls_period=1,
    min_seconds_between_calls=0.2,
)
async def get_json(
    session: ClientSession, endpoint: str, **kargs
) -> List[Dict[str, Any]]:
    """Get as JSON the result of a GET request to endpoint."""
    async with session.get(endpoint, **kargs) as response:
        log('info', f'[{response.status}] {endpoint}, {kargs["params"]}')
        response.raise_for_status()

        return await response.json()


async def get_json_less_than(
    target_id: int,
    session: ClientSession,
    endpoint: str, **kargs
) -> List[Dict[str, Any]]:
    """Get as JSON the result of a GET request to endpoint."""
    raw_data = await get_json(session, endpoint, **kargs)
    return elements_less_than(target_id, raw_data)


async def get_resource(
    session: ClientSession, resource: GitlabResourcePage
) -> List[Any]:
    endpoint = (
        'https://gitlab.com/api/v4/projects/'
        f'{resource.g_resource.project}/{resource.g_resource.resource}'
    )
    params = {
        'page': resource.page,
        'per_page': resource.per_page
    }
    async with session.get(endpoint, params=params) as response:
        response.raise_for_status()
        return await response.json()


def elements_less_than(
    target_id: int, data: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for item in data:
        if item['id'] < target_id:
            result.append(item)
    return result


def build_getter(
    less_than: Optional[int]
) -> Callable[..., Coroutine[Any, Any, List[Dict[str, Any]]]]:
    if less_than is not None:

        async def filtered_getter(
            session: ClientSession, endpoint: str, **kargs
        ) -> List[Dict[str, Any]]:
            return await get_json_less_than(
                cast(int, less_than), session, endpoint, **kargs
            )

        return filtered_getter

    async def normal_getter(
        session: ClientSession, endpoint: str, **kargs
    ) -> List[Dict[str, Any]]:
        return await get_json(session, endpoint, **kargs)

    return normal_getter
