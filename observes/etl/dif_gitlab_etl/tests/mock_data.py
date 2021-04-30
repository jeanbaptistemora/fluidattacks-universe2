# Standard libraries
from tempfile import NamedTemporaryFile
from typing import (
    Callable,
    NamedTuple,
    cast,
    Dict,
    IO,
    List,
    Optional,
    Union,
)

# Third party libraries
# Local libraries
from dif_gitlab_etl.etl import ExtractState
from streamer_gitlab.api_client import (
    GitlabResource,
    GitlabResourcePage,
    GResourcePageRange,
)
from streamer_gitlab.page_data import PageData


class MockDataCase(NamedTuple):
    resource: GitlabResourcePage
    gr_pages: List[GitlabResourcePage]
    data_pages: List[PageData]
    gr_dpag_mapper: Dict[GitlabResourcePage, PageData]
    min_id: Dict[str, int]
    pages_range: range
    mock_temp_files: Dict[str, IO[str]] = {}


def mock_create_temp(mock_data: MockDataCase) -> Callable[[str], IO[str]]:
    def _mock_create_temp(path: str) -> IO[str]:
        file = NamedTemporaryFile(mode="w+")
        mock_data.mock_temp_files[path] = file
        return file

    return _mock_create_temp


def mock_get_temp(mock_data: MockDataCase) -> Callable[[str], IO[str]]:
    def _mock_get_temp(path: str) -> IO[str]:
        return mock_data.mock_temp_files[path]

    return _mock_get_temp


def mock_extract_data(
    mock_data: MockDataCase,
) -> Callable[[GitlabResourcePage], Union[PageData, None]]:
    def _mock_extract_data(resource: GitlabResourcePage) -> PageData:
        try:
            return PageData(
                id=resource,
                file=mock_create_temp(mock_data)(
                    f"case_01/page_{resource.page}"
                ),
                minor_item_id=mock_data.min_id[str(resource.page)],
            )
        except KeyError:
            return None

    return _mock_extract_data


def mock_case_01() -> MockDataCase:
    case: MockDataCase = MockDataCase(
        resource=None,
        gr_pages=[],
        data_pages=[],
        gr_dpag_mapper=dict(),
        min_id=dict(),
        pages_range=range(0),
    )
    resource = GitlabResource(project="test_case_01", resource="foo")
    gr_pages: List[GitlabResourcePage] = []
    data_pages: List[PageData] = []
    gr_dpag_mapper: Dict[GitlabResourcePage, PageData] = {}
    min_id: Dict[str, int] = {
        "1": 41,
        "2": 36,
        "3": 31,
        "4": 26,
        "5": 21,
        "6": 16,
        "7": 11,
        "8": 6,
        "9": 1,
    }
    pages: range = range(1, 10)

    for page in pages:
        gr_page = GitlabResourcePage(
            g_resource=resource, page=page, per_page=5
        )
        gr_pages.append(gr_page)

        temp_file = mock_create_temp(case)(f"case_01/page_{page}")

        dpage = PageData(
            id=gr_pages[-1],
            file=temp_file,
            minor_item_id=min_id[str(page)],
        )
        data_pages.append(dpage)

        gr_dpag_mapper[gr_page] = dpage
    mock_case = MockDataCase(
        **dict(
            case._asdict(),
            resource=resource,
            gr_pages=gr_pages,
            data_pages=data_pages,
            gr_dpag_mapper=gr_dpag_mapper,
            min_id=min_id,
            pages_range=pages,
        )
    )
    return mock_case


def mock_extract_data_less_than(
    mock_data: MockDataCase,
) -> Callable[[int, GitlabResourcePage], Union[PageData, None]]:
    def _mock_extract_data_less_than(
        target_id: int, resource: GitlabResourcePage
    ) -> Union[PageData, None]:
        if (
            resource.g_resource == mock_data.resource
            and resource.page in mock_data.pages_range
        ):
            return PageData(
                id=resource,
                file=mock_create_temp(mock_data)(
                    f"case_01/page_{resource.page}_less_than_{target_id}"
                ),
                minor_item_id=mock_data.min_id[str(resource.page)],
            )
        return None

    return _mock_extract_data_less_than


def mock_extract_between(
    mock_data: MockDataCase,
) -> Callable[[GResourcePageRange, Optional[int]], ExtractState]:
    def _mock_extract_between(
        resource_range: GResourcePageRange, init_last_minor_id: Optional[int]
    ) -> ExtractState:
        last_page_reached = False
        pages: List[PageData] = []
        last_minor_id: Optional[int] = init_last_minor_id
        for page in resource_range.page_range:
            if last_minor_id is None:
                dpage = mock_extract_data(mock_data)(
                    GitlabResourcePage(
                        g_resource=resource_range.g_resource,
                        per_page=resource_range.per_page,
                        page=page,
                    )
                )
            else:
                dpage = mock_extract_data_less_than(mock_data)(
                    last_minor_id,
                    GitlabResourcePage(
                        g_resource=resource_range.g_resource,
                        per_page=resource_range.per_page,
                        page=page,
                    ),
                )
            if not dpage:
                last_page_reached = True
                break
            pages.append(dpage)
            candidate = pages[-1].minor_item_id
            if not last_minor_id or candidate < last_minor_id:
                last_minor_id = candidate

        return ExtractState(
            pages,
            cast(int, last_minor_id),
            last_page_reached,
        )

    return _mock_extract_between
