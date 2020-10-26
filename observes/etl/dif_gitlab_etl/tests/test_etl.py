# Standard libraries
from typing import (
    List,
)
# Third party libraries
import pytest
# Local libraries
from dif_gitlab_etl import etl
from dif_gitlab_etl.etl import ExtractState
from tests import mock_data
from streamer_gitlab.api_client import (
    GitlabResource,
    GitlabResourcePage,
    GResourcePageRange,
)
from streamer_gitlab.extractor import PageData



def test_extract_between():
    # Arrange
    case = mock_data.mock_case_01()
    # Act
    extract_status: etl.ExtractState = etl.extract_between(
        resource_range=GResourcePageRange(
            g_resource=case.resource,
            page_range=range(5,8),
            per_page=100,
        ),
        extract_data=mock_data.mock_extract_data(case),
        extract_data_less_than=mock_data.mock_extract_data_less_than(case),
    )
    # Assert
    def page(num: int) -> GitlabResourcePage:
        return GitlabResourcePage(
            g_resource=case.resource, page=num, per_page=100
        )

    expected: List[PageData] = [
        PageData(
            id=page(5),
            minor_item_id=case.min_id['5'],
            file=mock_data.mock_get_temp(case)(
                'case_01/page_5'
            )
        ),
        PageData(
            id=page(6), minor_item_id=case.min_id['6'],
            file=mock_data.mock_get_temp(case)(
                f"case_01/page_6_less_than_{case.min_id['5']}"
            )
        ),
        PageData(
            id=page(7), minor_item_id=case.min_id['7'],
            file=mock_data.mock_get_temp(case)(
                f"case_01/page_7_less_than_{case.min_id['6']}"
            )
        ),
    ]
    assert extract_status.data_pages == expected
    assert extract_status.last_minor_id == case.min_id['7']


@pytest.mark.timeout(10)
def test_extract_until_found():
    # Arrange
    case = mock_data.mock_case_01()
    # Act
    extract_status: etl.ExtractState = etl.extract_until_found(
        target_id=case.min_id['2'] + 2,
        start_resource_page=GitlabResourcePage(
            g_resource=case.resource,
            page=1, per_page=100,
        ),
        extract_range=mock_data.mock_extract_between(case)
    )
    # Assert
    def page(num: int) -> GitlabResourcePage:
        return GitlabResourcePage(
            g_resource=case.resource, page=num, per_page=100
        )

    expected: List[PageData] = [
        PageData(
            id=page(1), minor_item_id=case.min_id['1'],
            file=mock_data.mock_get_temp(case)(
                f"case_01/page_1"
            ),
        ),
        PageData(
            id=page(2), minor_item_id=case.min_id['2'],
            file=mock_data.mock_get_temp(case)(
                f"case_01/page_2_less_than_{case.min_id['1']}"
            ),
        ),
    ]
    assert extract_status.data_pages == expected
    assert extract_status.last_minor_id == case.min_id['2']


@pytest.mark.timeout(10)
def test_extract_until_found_last_page():
    # Arrange
    case = mock_data.mock_case_01()
    # Act
    extract_status: etl.ExtractState = etl.extract_until_found(
        target_id=0,
        start_resource_page=GitlabResourcePage(
            g_resource=case.resource,
            page=8, per_page=100,
        ),
        extract_range=mock_data.mock_extract_between(case)
    )
    # Assert
    def page(num: int) -> GitlabResourcePage:
        return GitlabResourcePage(
            g_resource=case.resource, page=num, per_page=100
        )

    expected: List[PageData] = [
        PageData(
            id=page(8), minor_item_id=case.min_id['8'],
            file=mock_data.mock_get_temp(case)(
                f"case_01/page_8"
            ),
        ),
        PageData(
            id=page(9), minor_item_id=case.min_id['9'],
            file=mock_data.mock_get_temp(case)(
                f"case_01/page_9_less_than_{case.min_id['8']}"
            ),
        ),
    ]
    assert extract_status.data_pages == expected
    assert extract_status.empty_responce == True
    assert extract_status.last_minor_id == case.min_id['9']
