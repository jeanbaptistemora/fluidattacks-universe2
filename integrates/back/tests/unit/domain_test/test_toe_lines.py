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
