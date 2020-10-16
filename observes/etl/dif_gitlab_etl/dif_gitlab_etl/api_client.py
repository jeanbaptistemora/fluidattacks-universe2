# Standard libraries
from typing import (
    Any,
    List,
    NamedTuple
)
# Third party libraries
from aiohttp import (
    ClientSession,
)
# Local libraries


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
