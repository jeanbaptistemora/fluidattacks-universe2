from dataloaders import (
    get_new_context,
)
from db_model.toe_lines.types import (
    ServicesToeLines,
)
import pytest
from toe.lines import (
    domain as toe_lines_domain,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_by_root() -> None:
    group_name = "unittesting"
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    loaders = get_new_context()
    root_toe_lines = await loaders.root_toe_lines.load((group_name, root_id))
    assert root_toe_lines == (
        ServicesToeLines(
            comments="comment test",
            filename="product/test/test#.config",
            group_name="unittesting",
            loc=8,
            modified_commit="983466z",
            modified_date="2019-08-01T00:00:00-05:00",
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            tested_date="2021-02-28T00:00:00-05:00",
            tested_lines=4,
            sorts_risk_level=0,
        ),
    )


@pytest.mark.changes_db
async def test_add() -> None:
    group_name = "unittesting"
    toe_lines = ServicesToeLines(
        comments="comment test",
        filename="product/test/new#.new",
        group_name=group_name,
        loc=4,
        modified_commit="983466z",
        modified_date="2019-08-01T00:00:00-05:00",
        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        tested_date="2021-02-28T00:00:00-05:00",
        tested_lines=12,
        sorts_risk_level=0,
    )
    await toe_lines_domain.add(toe_lines)
    loaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load(group_name)
    assert toe_lines in group_toe_lines


@pytest.mark.changes_db
async def test_remove() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load(group_name)
    assert len(group_toe_lines) == 3
    await toe_lines_domain.remove(
        group_name=group_name,
        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        filename="product/test/new#.new",
    )
    loaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load(group_name)
    assert len(group_toe_lines) == 2


@pytest.mark.changes_db
async def test_update() -> None:
    group_name = "unittesting"
    toe_lines = ServicesToeLines(
        comments="edited",
        filename="product/test/test#.config",
        group_name="unittesting",
        loc=55,
        modified_commit="983466r",
        modified_date="2020-08-01T00:00:00-05:00",
        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        tested_date="2021-03-28T00:00:00-05:00",
        tested_lines=55,
        sorts_risk_level=0,
    )
    await toe_lines_domain.update(toe_lines)
    loaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load(group_name)
    assert toe_lines in group_toe_lines
