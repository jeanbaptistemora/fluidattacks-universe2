# Standard libraries
from os import environ
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List, Optional,
)
# Third party libraries
import aiohttp
# Local libraries
from streamer_gitlab.api_client import (
    GitlabResource,
    GitlabResourcePage,
)
from streamer_gitlab import api_client
from dif_gitlab_etl.utils import (
    log,
    NotFoundException,
)

# lgu = last greater uploaded


async def search_page_with(
    get_resource: Callable[[GitlabResourcePage], Awaitable],
    target_id: int,
    last_seen: GitlabResourcePage
) -> int:
    found: bool = False
    items: List[Dict[str, Any]] = []
    counter: int = 0
    while not found:
        items = await get_resource(
            GitlabResourcePage(
                g_resource=last_seen.g_resource,
                page=last_seen.page + counter,
                per_page=last_seen.per_page,
            )
        )
        minor_id: Optional[int] = api_client.get_minor_id(items)
        if minor_id:
            if minor_id > target_id:
                counter = counter + 1
                if counter % 100 == 0:
                    log('info', f'searching at offset {counter}*100')
            else:
                if counter == 0:
                    log('warning', 'page id could be incorrect')
                found = True
        else:
            log('info', 'page not found, default: last page returned')
            counter = counter - 1
            found = True
    return last_seen.page + counter


def calculate_interval(last_page_id: int, max_pages: int) -> range:
    init_page_id = 1
    if not last_page_id - max_pages < 1:
        init_page_id = last_page_id - max_pages
    return range(init_page_id, last_page_id + 1)


# integrated functions


async def get_lgu_id(
    resource: GitlabResource,
    exe_query: Callable[[str], Any]
) -> int:
    result = exe_query(
        "SELECT lgu_id FROM \"gitlab-ci\".upload_state "
        f"WHERE project='{resource.project}' "
        f"AND resource='{resource.resource}'"
    )
    if not result:
        raise NotFoundException(
            'Unknown lgu id for '
            f'{resource.project}/{resource.resource}'
        )
    log('debug', str(result))
    return result[0][0]


async def get_lgu_last_seen_page_id(
    resource: GitlabResource,
    exe_query: Callable[[str], Any]
) -> Dict[str, int]:
    result = exe_query(
        "SELECT last_seen_page,per_page FROM \"gitlab-ci\".upload_state "
        f"WHERE project='{resource.project}' "
        f"AND resource='{resource.resource}'"
    )
    if not result:
        raise NotFoundException(
            'Unknown last seen page for '
            f'{resource.project}/{resource.resource}'
        )
    log('debug', str(result))
    return {'page': result[0][0], 'per_page': result[0][1]}


async def get_work_interval(
    resource: GitlabResource,
    exe_query: Callable[[str], Any],
    max_pages: int = 10
) -> range:
    return calculate_interval(
        await search_lgu_page(resource, exe_query),
        max_pages
    )


async def search_lgu_page(
    resource: GitlabResource,
    exe_query: Callable[[str], Any]
) -> int:
    """
    Returns de id of a page where item_id is present
    """
    target_id: int = await get_lgu_id(resource, exe_query)
    last_seen: Dict[str, int] = await get_lgu_last_seen_page_id(
        resource, exe_query
    )
    log('info', 'Search lgu page started')
    async with aiohttp.ClientSession() as session:

        def build_get_resource(session):
            async def getter(resource):
                api_token = environ['GITLAB_API_TOKEN']
                headers = {'Private-Token': api_token}
                return await api_client.get_resource(
                    session, resource, headers=headers
                )
            return getter

        return await search_page_with(
            build_get_resource(session),
            target_id,
            GitlabResourcePage(
                g_resource=resource,
                page=last_seen['page'],
                per_page=last_seen['per_page'],
            )
        )
