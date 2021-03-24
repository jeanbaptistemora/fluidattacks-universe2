# Third party libraries
import pytest

# Local libraries
from backend.api import get_new_context
from dynamodb.types import (
    GitRootToeLines,
)
from toe.lines import domain as toe_lines_domain

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_by_group():
    group_name = 'unittesting'
    loaders = get_new_context()
    group_toe_lines = await toe_lines_domain.get_by_group(
        loaders, group_name
    )
    assert group_toe_lines == (
        GitRootToeLines(
            comments='comment test',
            filename='product/test/test.config',
            group_name='unittesting',
            loc=8,
            modified_commit='983466z',
            modified_date='2019-08-01 00:00:00',
            root_id='4039d098-ffc5-4984-8ed3-eb17bca98e19',
            tested_date='2021-02-28 00:00:00',
            tested_lines=4
        ),
        GitRootToeLines(
            comments='comment test',
            filename='integrates_1/test2/test.sh',
            group_name='unittesting',
            loc=120,
            modified_commit='273412t',
            modified_date='2020-11-19 00:00:00',
            root_id='765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a',
            tested_date='2021-01-20 00:00:00',
            tested_lines=172
        )
    )
