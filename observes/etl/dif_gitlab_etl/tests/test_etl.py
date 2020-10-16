# Standard libraries
# Third party libraries
import pytest
from typing import (
    List,
    Union,
)
# Local libraries
from dif_gitlab_etl.api_client import (
    GitlabResource,
    GitlabResourcePage,
    GResourcePageRange,
)
from dif_gitlab_etl import etl
from dif_gitlab_etl.etl import ExtractState
from dif_gitlab_etl.page_data import PageData


def mock_extract_data(resource: GitlabResourcePage) -> Union[PageData, None]:
    case_01 = GitlabResource(
        project='test_case_01',
        resource='foo'
    )
    if resource.g_resource == case_01:
        min_id = {'5': 401, '6': 351, '7': 270,}
        if resource.page > 7:
            return None
        return PageData(
            id=resource.page,
            path=f'case_01/page_{resource.page}',
            minor_item_id=min_id[str(resource.page)],
        )
    return None


def mock_extract_data_less_than(
    target_id: int,
    resource: GitlabResourcePage
) -> Union[PageData, None]:
    case_01 = GitlabResource(
        project='test_case_01',
        resource='foo'
    )
    if resource.g_resource == case_01:
        min_id = {'5': 401, '6': 351, '7': 270,}
        return PageData(
            id=resource.page,
            path=f'case_01/page_{resource.page}_less_than_{target_id}',
            minor_item_id=min_id[str(resource.page)],
        )
    return None


def test_extract_between():
    extract_status: etl.ExtractState = etl.extract_between(
        resource_range=GResourcePageRange(
            g_resource=GitlabResource(
                project='test_case_01',
                resource='foo'
            ),
            page_range=range(5,8),
            per_page=100,
        ),
        extract_data=mock_extract_data,
        extract_data_less_than=mock_extract_data_less_than,
    )
    expected: List[PageData] = [
        PageData(id=5, path='case_01/page_5', minor_item_id=401),
        PageData(id=6, path='case_01/page_6_less_than_401', minor_item_id=351),
        PageData(id=7, path='case_01/page_7_less_than_351', minor_item_id=270),
    ]
    assert extract_status.data_pages == expected
    assert extract_status.last_minor_id == 270


def mock_extract_range(
    resource_range: GResourcePageRange, init_last_minor_id: int
)-> ExtractState:
    last_page = 3
    last_page_reached = False
    pages: List[PageData] = []
    minor_ids = [201, 101, 1]

    for page in resource_range.page_range:
        if page > last_page:
            last_page_reached = True
            break
        pages.append(
            PageData(
                id=page,
                path=f'case_02/processed_page_{page}',
                minor_item_id=minor_ids[page - 1]
            )
        )

    last_page_in_rage = resource_range.page_range.stop - 1
    if  last_page_in_rage > last_page:
        last_minor_id = minor_ids[-1]
    else:
        last_minor_id = minor_ids[last_page_in_rage - 1]
    return ExtractState(
        pages, last_minor_id, last_page_reached
    )


@pytest.mark.timeout(10)
def test_extract_until_found():
    extract_status: etl.ExtractState = etl.extract_until_found(
        target_id=150,
        start_resource_page=GitlabResourcePage(
            g_resource=GitlabResource(
                project='test_case_02',
                resource='foo',
            ),
            page=1, per_page=100,
        ),
        extract_range=mock_extract_range
    )
    expected: List[PageData] = [
        PageData(id=1, path='case_02/processed_page_1', minor_item_id=201),
        PageData(id=2, path='case_02/processed_page_2', minor_item_id=101),
    ]
    assert extract_status.data_pages == expected
    assert extract_status.last_minor_id == 101


@pytest.mark.timeout(10)
def test_extract_until_found_last_page():
    extract_status: etl.ExtractState = etl.extract_until_found(
        target_id=0,
        start_resource_page=GitlabResourcePage(
            g_resource=GitlabResource(
                project='test_case_02',
                resource='foo',
            ),
            page=1, per_page=100,
        ),
        extract_range=mock_extract_range
    )
    expected: List[PageData] = [
        PageData(id=1, path='case_02/processed_page_1', minor_item_id=201),
        PageData(id=2, path='case_02/processed_page_2', minor_item_id=101),
        PageData(id=3, path='case_02/processed_page_3', minor_item_id=1),
    ]
    assert extract_status.data_pages == expected
    assert extract_status.empty_responce == True
    assert extract_status.last_minor_id == 1
