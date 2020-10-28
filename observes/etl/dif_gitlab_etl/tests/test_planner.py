# Standard libraries
# Third party libraries
import pytest
# Local libraries
from dif_gitlab_etl import planner
from dif_gitlab_etl.utils import NotFoundException
from streamer_gitlab.api_client import (
    GitlabResource,
    GitlabResourcePage,
)


############### `search_page_with` Tests ###############
def mock_get_resource(resource: GitlabResourcePage):
    if resource.page == 123:
        return [
            {'id': '245'}, {'id': '244'}, {'id': '243'}
        ]
    if resource.page < 123:
        return [
            {'id': '250'}, {'id': '249'}, {'id': '248'}
        ]
    if resource.page > 123 and resource.page <= 130:
        return [
            {'id': '242'}, {'id': '241'}, {'id': '240'}
        ]
    return None


def test_search_page_with():
    """
    Should return the page where `target_id` is present
    """
    page_id = planner.search_page_with(
        get_resource=mock_get_resource,
        target_id=243,
        last_seen=GitlabResourcePage(
            GitlabResource(
                project='projet64',
                resource='athernos',
            ),
            page=111,
            per_page=3,
        ),
    )
    assert page_id == 123


def test_search_page_last_page():
    """
    Should return the last page when `target_id` is not found
    """
    page_id = planner.search_page_with(
        get_resource=mock_get_resource,
        target_id=0,
        last_seen=GitlabResourcePage(
            GitlabResource(
                project='projet64',
                resource='athernos',
            ),
            page=111,
            per_page=3,
        ),
    )
    assert page_id == 130


def mock_fail_get_resource(resource: GitlabResourcePage):
    if resource.page >= 111:
        return [
            {'id': '300'}
        ]
    if resource.page < 111:
        raise Exception('Should not get pages below last_seen')


def test_not_start_from_scratch():
    """
    Should start iterating from `last_seen.page`
    """
    planner.search_page_with(
        get_resource=mock_fail_get_resource,
        target_id=300,
        last_seen=GitlabResourcePage(
            GitlabResource(
                project='projet64',
                resource='athernos',
            ),
            page=111,
            per_page=3,
        )
    )


############### `calculate_interval` Tests ###############
def test_calculate_interval_len():
    """
    Should return a range with `max_pags` elements
    """
    final_id = 1255
    max_pags = 25
    interval = planner.calculate_interval(final_id, max_pags)
    assert len(interval) == max_pags


def test_calculate_interval_stop():
    """
    Should return a range ending at `final_id`
    """
    final_id = 2432
    max_pags = 56
    interval = planner.calculate_interval(final_id, max_pags)
    assert interval.stop == final_id + 1


def test_calculate_interval_start_min():
    """
    Should return a minimun start page of 1
    """
    final_id = 10
    max_pags = 25
    interval = planner.calculate_interval(final_id, max_pags)
    assert interval.start == 1


############### `get_lgu_id` Tests ###############
def mock_resource():
    return GitlabResource(
        project='projet64',
        resource='athernos',
    )

def test_get_lgu_id_fail():
    """
    Should raise a NotFoundException
    """
    with pytest.raises(NotFoundException):
        planner.get_lgu_id(mock_resource(), lambda x: None)


def test_get_lgu_id_expected():
    """
    Should process returned value
    """
    result = planner.get_lgu_id(mock_resource(), lambda x: ((34,),))
    assert result == 34


############### `get_lgu_last_seen_page_id` Tests ###############
def test_get_lgu_last_seen_page_id_fail():
    """
    Should raise a NotFoundException
    """
    with pytest.raises(NotFoundException):
        planner.get_lgu_last_seen_page_id(mock_resource(), lambda x: None)



def test_get_lgu_last_seen_page_id_expected():
    """
    Should return expected data
    """
    result = planner.get_lgu_last_seen_page_id(
        mock_resource(), lambda x: ((12,45),)
    )
    assert result == {'page': 12, 'per_page': 45}
