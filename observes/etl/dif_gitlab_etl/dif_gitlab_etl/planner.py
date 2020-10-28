# Standard libraries
import asyncio
from os import environ
from typing import (
    Any,
    Callable,
    Dict,
    List, Optional,
)
# Third party libraries
from aiohttp import ClientSession
# Local libraries
from streamer_gitlab import api_client
from streamer_gitlab.api_client import (
    GitlabResource,
    GitlabResourcePage,
)
from streamer_gitlab.page_data import PageData
from dif_gitlab_etl.utils import (
    log,
    NotFoundException,
)

# lgu = last greater uploaded


def search_page_with(
    get_resource: Callable[[GitlabResourcePage], List[Dict[str, Any]]],
    target_id: int,
    last_seen: GitlabResourcePage
) -> int:
    found: bool = False
    items: List[Dict[str, Any]] = []
    counter: int = 0
    log('info', f'lgu last seen page: {last_seen.page}')
    while not found:
        items = get_resource(
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
                log('info', f'searching at offset {counter}')
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


def get_lgu_id(
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


def get_lgu_last_seen_page_id(
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


def set_lgu_id(
    dpage: PageData,
    exe_query: Callable[[str], Any]
):
    result = exe_query(
        "UPDATE \"gitlab-ci\".upload_state set "
        f"lgu_id={dpage.minor_item_id}, "
        f"last_seen_page={dpage.id.page}, "
        f"per_page={dpage.id.per_page} "
        f"WHERE project='{dpage.id.g_resource.project}' "
        f"AND resource='{dpage.id.g_resource.resource}'"
    )
    log('debug', str(result))


def get_work_interval(
    resource: GitlabResource,
    exe_query: Callable[[str], Any],
    max_pages: int = 10
) -> range:
    loop = asyncio.get_event_loop()
    return calculate_interval(
        loop.run_until_complete(
            search_lgu_page(resource, exe_query)
        ),
        max_pages
    )


async def search_lgu_page(
    resource: GitlabResource,
    exe_query: Callable[[str], Any]
) -> int:
    """
    Returns de id of a page where item_id is present
    """
    target_id: int = get_lgu_id(resource, exe_query)
    last_seen: Dict[str, int] = get_lgu_last_seen_page_id(
        resource, exe_query
    )
    log('info', 'Search lgu page started')

    async with ClientSession() as session:
        def build_get_resource(
            session: ClientSession
        ) -> Callable[[GitlabResourcePage], List[Dict[str, Any]]]:
            def getter(resource):
                api_token = environ['GITLAB_API_TOKEN']
                headers = {'Private-Token': api_token}
                loop = asyncio.get_event_loop()
                return loop.run_until_complete(
                    api_client.get_resource(
                        session, resource, headers=headers
                    )
                )
            return getter

        return search_page_with(
            build_get_resource(session),
            target_id,
            GitlabResourcePage(
                g_resource=resource,
                page=last_seen['page'],
                per_page=last_seen['per_page'],
            )
        )
