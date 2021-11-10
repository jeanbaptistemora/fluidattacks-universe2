from dataloaders import (
    get_new_context,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from freezegun import (  # type: ignore
    freeze_time,
)
import pytest
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToAdd,
    ToeLinesAttributesToUpdate,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@freeze_time("2018-08-01T05:00:00+00:00")
@pytest.mark.changes_db
async def test_add() -> None:
    group_name = "unittesting"
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    filename = "product/test/new#.new"
    attributes = ToeLinesAttributesToAdd(
        attacked_at="2020-08-01T05:00:00+00:00",
        attacked_by="hacker@test.com",
        attacked_lines=433,
        be_present=True,
        comments="comment test",
        commit_author="customer@gmail.com",
        first_attack_at="2020-04-01T05:00:00+00:00",
        loc=1000,
        modified_commit="983466z",
        modified_date="2019-08-01T05:00:00+00:00",
        sorts_risk_level=100,
    )
    await toe_lines_domain.add(group_name, root_id, filename, attributes)
    loaders = get_new_context()
    toe_lines = await loaders.toe_lines.load((group_name, root_id, filename))
    assert toe_lines == ToeLines(
        attacked_at="2020-08-01T05:00:00+00:00",
        attacked_by="hacker@test.com",
        attacked_lines=433,
        be_present=True,
        comments="comment test",
        commit_author="customer@gmail.com",
        filename="product/test/new#.new",
        first_attack_at="2020-04-01T05:00:00+00:00",
        group_name="unittesting",
        loc=1000,
        modified_commit="983466z",
        modified_date="2019-08-01T05:00:00+00:00",
        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        seen_at="2018-08-01T05:00:00+00:00",
        sorts_risk_level=100,
    )


@pytest.mark.changes_db
async def test_update() -> None:
    group_name = "unittesting"
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    filename = "product/test/new#.new"
    loaders = get_new_context()
    current_value = await loaders.toe_lines.load(
        (group_name, root_id, filename)
    )
    attributes = ToeLinesAttributesToUpdate(
        attacked_at="2022-08-01T05:00:00+00:00",
        attacked_by="hacker2@test.com",
        attacked_lines=434,
        be_present=False,
        comments="comment test 2",
        commit_author="customer2@gmail.com",
        first_attack_at="2021-04-01T05:00:00+00:00",
        loc=1111,
        modified_commit="993466z",
        modified_date="2020-08-01T05:00:00+00:00",
        seen_at="2019-08-01T05:00:00+00:00",
        sorts_risk_level=50,
    )
    await toe_lines_domain.update(current_value, attributes)
    loaders = get_new_context()
    toe_lines = await loaders.toe_lines.load((group_name, root_id, filename))
    assert toe_lines == ToeLines(
        attacked_at="2022-08-01T05:00:00+00:00",
        attacked_by="hacker2@test.com",
        attacked_lines=434,
        be_present=False,
        comments="comment test 2",
        commit_author="customer2@gmail.com",
        filename="product/test/new#.new",
        first_attack_at="2021-04-01T05:00:00+00:00",
        group_name="unittesting",
        loc=1111,
        modified_commit="993466z",
        modified_date="2020-08-01T05:00:00+00:00",
        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        seen_at="2019-08-01T05:00:00+00:00",
        sorts_risk_level=50,
    )
