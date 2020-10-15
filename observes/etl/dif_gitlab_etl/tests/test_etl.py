# Standard libraries
# Third party libraries
from typing import (
    List,
    Union,
)
# Local libraries
from dif_gitlab_etl.api_client import (
    GitlabResource,
    GitlabResourcePage,
)
from dif_gitlab_etl import etl
from dif_gitlab_etl.page_data import PageData


def mock_extract_data(resource: GitlabResourcePage) -> Union[PageData, None]:
    case_01 = GitlabResource(
        project='test_case_01',
        resource='foo'
    )
    if resource.g_resource == case_01:
        return PageData(
            id=resource.page, path=f'case_01/page_{resource.page}'
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
        return PageData(
            id=resource.page, path=f'case_01/page_{resource.page}_less_than_{target_id}'
        )
    return None


def mock_get_minor_id(p_data: PageData) -> int:
    mapper = {
        'case_01/page_5': 401,
        'case_01/page_6_less_than_401': 351,
        'case_01/page_7_less_than_351': 270,
    }
    return mapper[p_data.path]


def test_extract_between():
    extract_status: etl.ExtractState = etl.extract_between(
        work_pages=range(5,8),
        resource=GitlabResource(
            project='test_case_01',
            resource='foo'
        ),
        per_page=100,
        extract_data=mock_extract_data,
        extract_data_less_than=mock_extract_data_less_than,
        get_minor_id=mock_get_minor_id
    )
    expected: List[PageData] = [
        PageData(id=5, path='case_01/page_5'),
        PageData(id=6, path='case_01/page_6_less_than_401'),
        PageData(id=7, path='case_01/page_7_less_than_351'),
    ]
    assert extract_status.data_pages == expected
    assert extract_status.last_minor_id == 270
