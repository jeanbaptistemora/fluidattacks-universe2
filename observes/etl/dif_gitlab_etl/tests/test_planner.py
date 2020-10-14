# Standard libraries
# Third party libraries
import pytest
# Local libraries
from dif_gitlab_etl.api_client import (
    GitlabResource,
    GitlabResourcePage,
)
from dif_gitlab_etl import planner


async def mock_get_resource(resource: GitlabResourcePage):
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


@pytest.mark.asyncio
async def test_search_page_with():
    page_id = await planner.search_page_with(
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


@pytest.mark.asyncio
async def test_search_page_last_page():
    page_id = await planner.search_page_with(
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
    assert page_id == 130  # expected last page


async def mock_fail_get_resource(resource: GitlabResourcePage):
    if resource.page >= 111:
        return [
            {'id': '300'}
        ]
    if resource.page < 111:
        raise Exception('Should not get pages below last_seen')


@pytest.mark.asyncio
async def test_not_start_from_scratch():
    await planner.search_page_with(
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


def test_calculate_interval():
    final_id = 5000
    max_pags = 25
    interval = planner.calculate_interval(final_id, max_pags)
    assert interval.start == final_id - max_pags
    assert interval.stop == final_id + 1


def test_calculate_interval_start_min():
    final_id = 10
    max_pags = 25
    interval = planner.calculate_interval(final_id, max_pags)
    assert interval.start == 1
    assert interval.stop == final_id + 1
