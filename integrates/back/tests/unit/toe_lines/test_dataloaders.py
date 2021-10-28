from dataloaders import (
    get_new_context,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from decimal import (
    Decimal,
)
import pytest

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_by_group() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load(group_name)
    assert group_toe_lines == (
        ToeLines(
            attacked_at="2021-02-20T05:00:00+00:00",
            attacked_by="test2@test.com",
            attacked_lines=4,
            be_present=True,
            comments="comment 1",
            filename="test/test#.config",
            first_attack_at="2020-02-19T15:41:04+00:00",
            group_name="unittesting",
            loc=8,
            modified_commit="983466z",
            modified_date="2020-11-15T15:41:04+00:00",
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            seen_at="2020-02-01T15:41:04+00:00",
            sorts_risk_level=Decimal("0.8"),
        ),
        ToeLines(
            attacked_at="2021-01-20T05:00:00+00:00",
            attacked_by="test@test.com",
            attacked_lines=120,
            be_present=False,
            comments="comment 2",
            filename="test2/test.sh",
            first_attack_at="2020-01-19T15:41:04+00:00",
            group_name="unittesting",
            loc=172,
            modified_commit="273412t",
            modified_date="2020-11-16T15:41:04+00:00",
            root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            seen_at="2020-01-01T15:41:04+00:00",
            sorts_risk_level=Decimal("0.0"),
        ),
    )


async def test_get_by_root() -> None:
    group_name = "unittesting"
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    loaders = get_new_context()
    root_toe_lines = await loaders.root_toe_lines.load((group_name, root_id))
    assert root_toe_lines == (
        ToeLines(
            attacked_at="2021-02-20T05:00:00+00:00",
            attacked_by="test2@test.com",
            attacked_lines=4,
            be_present=True,
            comments="comment 1",
            filename="test/test#.config",
            first_attack_at="2020-02-19T15:41:04+00:00",
            group_name="unittesting",
            loc=8,
            modified_commit="983466z",
            modified_date="2020-11-15T15:41:04+00:00",
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            seen_at="2020-02-01T15:41:04+00:00",
            sorts_risk_level=Decimal("0.8"),
        ),
    )
