# Standard libraries
import pytest
from typing import (
    Any,
    Dict
)

# Local libraries
from . import (
    query,
    query_get
)
from .constants import USERS_EMAILS


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_toe_lines_sorts')
@pytest.mark.parametrize(['email'], USERS_EMAILS)
async def test_update_toe_lines_sorts(populate: bool, email: str):
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        group_name='group1',
        filename='integrates_1/test2/test.sh',
        sorts_risk_level=10
    )
    assert result['data']['updateToeLinesSorts']['success']
    result: Dict[str, Any] = await query_get(user=email, group_name='group1')
    assert result['data']['group']['roots'] == [
        {
            'id': '63298a73-9dff-46cf-b42d-9b2f01a56690',
            'toeLines': [
                {
                    'filename': 'product/test/test#.config',
                    'modifiedDate': '2019-08-01T00:00:00-05:00',
                    'modifiedCommit': '983466z',
                    'loc': 8,
                    'testedDate': '2021-02-28T00:00:00-05:00',
                    'testedLines': 4,
                    'comments': 'comment test',
                    'sorts_risk_level': 0
                }
            ]
        },
        {
            'id': '765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a',
            'toeLines': [
                {
                    'filename': 'integrates_1/test2/test.sh',
                    'modifiedDate': '2020-11-19T00:00:00-05:00',
                    'modifiedCommit': '273412t',
                    'loc': 120,
                    'testedDate': '2021-01-20T00:00:00-05:00',
                    'testedLines': 172,
                    'comments': 'comment test',
                    'sorts_risk_level': 10
                },
                {
                    'filename': 'integrates_1/test3/test.config',
                    'modifiedDate': '2020-11-19T00:00:00-05:00',
                    'modifiedCommit': 'g545435i',
                    'loc': 55,
                    'testedDate': '2021-01-20T00:00:00-05:00',
                    'testedLines': 33,
                    'comments': 'comment test',
                    'sorts_risk_level': 0
                }
            ]
        }
    ]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('update_toe_lines_sorts')
@pytest.mark.parametrize(['email'], USERS_EMAILS)
async def test_update_toe_lines_sorts_no_filename(populate: bool, email: str):
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        group_name='group1',
        filename='non_existing_filename',
        sorts_risk_level=10
    )
    assert not result['data']['updateToeLinesSorts']['success']
