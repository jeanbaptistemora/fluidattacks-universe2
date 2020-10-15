# Standard libraries
from typing import (
    Callable,
    cast,
    List,
    NamedTuple,
    Union,
)
# Third party libraries
# Local libraries
from dif_gitlab_etl.api_client import (
    GitlabResource,
    GitlabResourcePage
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


def extract_between(  # pylint: disable=too-many-arguments
    work_pages: range,
    resource: GitlabResource,
    per_page: int,
    extract_data: Callable[[GitlabResourcePage], PageData],
    extract_data_less_than: Callable[[int, GitlabResourcePage], PageData],
    get_minor_id: Callable[[PageData], int],
) -> ExtractState:
    """
    Calls extract procedure and its filtered version
    taking into account the dynamic offset of the data.
    """
    pages: List[PageData] = []
    last_minor_id: Union[int, None] = None
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
