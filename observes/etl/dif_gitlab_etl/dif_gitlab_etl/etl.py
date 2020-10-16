# Standard libraries
from typing import (
    Callable,
    cast,
    List,
    NamedTuple,
    Optional,
)
# Third party libraries
# Local libraries
from dif_gitlab_etl.api_client import (
    GitlabResource,
    GitlabResourcePage,
    GResourcePageRange,
)
from dif_gitlab_etl.page_data import (
    PageData,
)
from dif_gitlab_etl.utils import (
    error,
    log,
)


class ExtractState(NamedTuple):
    data_pages: List[PageData]
    last_minor_id: int
    empty_responce: bool


def extract_between(
    resource_range: GResourcePageRange,
    extract_data: Callable[[GitlabResourcePage], PageData],
    extract_data_less_than: Callable[[int, GitlabResourcePage], PageData],
    get_minor_id: Callable[[PageData], int],
    init_last_minor_id: Optional[int] = None
) -> ExtractState:
    """
    Calls extract procedure and its filtered version over work_pages
    taking into account the dynamic offset of the data.
    """
    work_pages = resource_range.page_range
    resource = resource_range.g_resource
    per_page = resource_range.per_page

    pages: List[PageData] = []
    last_minor_id: Optional[int] = init_last_minor_id
    p_data: PageData
    log('info', 'Notation <page_id>:<per_page>')
    for page_id in work_pages:
        log('info', f'Extracting {page_id}:{per_page}')
        if last_minor_id is not None:
            p_data = extract_data_less_than(
                last_minor_id,
                GitlabResourcePage(
                    g_resource=resource,
                    page=page_id,
                    per_page=per_page,
                )
            )
        else:
            p_data = extract_data(
                GitlabResourcePage(
                    g_resource=resource,
                    page=page_id,
                    per_page=per_page,
                )
            )
        if p_data is None:
            error(f'Unexpected empty data at {page_id}:{per_page}')
        last_minor_id = get_minor_id(p_data)
        pages.append(p_data)
    return ExtractState(
        data_pages=pages,
        last_minor_id=cast(int, last_minor_id),
        empty_responce=False
    )


def extract_until_found(
    target_id: int,
    start_resource_page: GitlabResourcePage,
    extract_range: Callable[[GResourcePageRange, Optional[int]], ExtractState]
) -> ExtractState:
    """
    Executes extract_range over dynamic range until target_id is found
    or the last page is reached
    """
    start_page: int = start_resource_page.page
    per_page: int = start_resource_page.per_page
    resource: GitlabResource = start_resource_page.g_resource

    pages: List[PageData] = []
    last_minor_id: Optional[int] = None
    target_reached: bool = False
    last_data_reached: bool = False
    counter: int = 0
    while not target_reached and not last_data_reached:
        page_id = start_page + counter
        extract_status = extract_range(
            GResourcePageRange(
                g_resource=resource,
                page_range=range(page_id, page_id + 1),
                per_page=per_page
            ),
            last_minor_id
        )
        if extract_status.empty_responce:
            last_data_reached = True
            continue
        if target_id > extract_status.last_minor_id:
            target_reached = True
        pages.extend(extract_status.data_pages)
        last_minor_id = extract_status.last_minor_id
        counter = counter + 1
    return ExtractState(
        data_pages=pages,
        last_minor_id=cast(int, last_minor_id),
        empty_responce=last_data_reached
    )
