# Third party libraries
import pytest

# Local libraries
from data_containers.toe_lines import GitRootToeLines
from toe.lines import domain as toe_lines_domain

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_by_group():
    group_name = 'unittesting'
    group_toe_lines = await toe_lines_domain.get_by_group(group_name)
    assert group_toe_lines == (
        GitRootToeLines(
            comments='comment test',
            filename='product/test/test#.config',
            group_name='unittesting',
            loc=8,
            modified_commit='983466z',
            modified_date='2019-08-01T00:00:00-05:00',
            root_id='4039d098-ffc5-4984-8ed3-eb17bca98e19',
            tested_date='2021-02-28T00:00:00-05:00',
            tested_lines=4,
            sorts_risk_level=0,
        ),
        GitRootToeLines(
            comments='comment test',
            filename='integrates_1/test2/test.sh',
            group_name='unittesting',
            loc=120,
            modified_commit='273412t',
            modified_date='2020-11-19T00:00:00-05:00',
            root_id='765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a',
            tested_date='2021-01-20T00:00:00-05:00',
            tested_lines=172,
            sorts_risk_level=0,
        )
    )


async def test_get_by_root():
    group_name = 'unittesting'
    root_id = '4039d098-ffc5-4984-8ed3-eb17bca98e19'
    root_toe_lines = await toe_lines_domain.get_by_root(
        group_name, root_id
    )
    assert root_toe_lines == (
        GitRootToeLines(
            comments='comment test',
            filename='product/test/test#.config',
            group_name='unittesting',
            loc=8,
            modified_commit='983466z',
            modified_date='2019-08-01T00:00:00-05:00',
            root_id='4039d098-ffc5-4984-8ed3-eb17bca98e19',
            tested_date='2021-02-28T00:00:00-05:00',
            tested_lines=4,
            sorts_risk_level=0,
        ),
    )


@pytest.mark.changes_db
async def test_add() -> None:
    group_name = 'unittesting'
    toe_lines = GitRootToeLines(
        comments='comment test',
        filename='product/test/new#.new',
        group_name=group_name,
        loc=4,
        modified_commit='983466z',
        modified_date='2019-08-01T00:00:00-05:00',
        root_id='4039d098-ffc5-4984-8ed3-eb17bca98e19',
        tested_date='2021-02-28T00:00:00-05:00',
        tested_lines=12,
        sorts_risk_level=0,
    )
    await toe_lines_domain.add(toe_lines)
    group_toe_lines = await toe_lines_domain.get_by_group(group_name)
    assert toe_lines in group_toe_lines


@pytest.mark.changes_db
async def test_delete() -> None:
    group_name = 'unittesting'
    group_toe_lines = await toe_lines_domain.get_by_group(group_name)
    assert len(group_toe_lines) == 3
    await toe_lines_domain.delete(
        group_name=group_name,
        root_id='4039d098-ffc5-4984-8ed3-eb17bca98e19',
        filename='product/test/new#.new',
    )
    group_toe_lines = await toe_lines_domain.get_by_group(group_name)
    assert len(group_toe_lines) == 2


@pytest.mark.changes_db
async def test_update() -> None:
    group_name = 'unittesting'
    toe_lines = GitRootToeLines(
        comments='edited',
        filename='product/test/test#.config',
        group_name='unittesting',
        loc=55,
        modified_commit='983466r',
        modified_date='2020-08-01T00:00:00-05:00',
        root_id='4039d098-ffc5-4984-8ed3-eb17bca98e19',
        tested_date='2021-03-28T00:00:00-05:00',
        tested_lines=55,
        sorts_risk_level=0,
    )
    await toe_lines_domain.update(toe_lines)
    group_toe_lines = await toe_lines_domain.get_by_group(group_name)
    assert toe_lines in group_toe_lines
