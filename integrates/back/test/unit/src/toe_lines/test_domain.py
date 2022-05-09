from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    ToeLines,
    ToeLinesRequest,
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


@pytest.mark.changes_db
@freeze_time("2018-08-01T05:00:00+00:00")
async def test_add() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    filename = "product/test/new#.new"
    attributes = ToeLinesAttributesToAdd(
        attacked_at=datetime.fromisoformat("2020-08-01T05:00:00+00:00"),
        attacked_by="hacker@test.com",
        attacked_lines=433,
        comments="comment test",
        last_author="user@gmail.com",
        has_vulnerabilities=False,
        loc=1000,
        last_commit="983466z",
        modified_date=datetime.fromisoformat("2019-08-01T05:00:00+00:00"),
        sorts_risk_level=100,
    )
    await toe_lines_domain.add(
        loaders, group_name, root_id, filename, attributes
    )
    loaders = get_new_context()
    toe_lines = await loaders.toe_lines.load(
        ToeLinesRequest(
            group_name=group_name, root_id=root_id, filename=filename
        )
    )
    assert toe_lines == ToeLines(
        attacked_at=datetime.fromisoformat("2020-08-01T05:00:00+00:00"),
        attacked_by="hacker@test.com",
        attacked_lines=0,
        be_present=True,
        be_present_until=None,
        comments="comment test",
        filename="product/test/new#.new",
        first_attack_at=datetime.fromisoformat("2020-08-01T05:00:00+00:00"),
        group_name="unittesting",
        has_vulnerabilities=False,
        last_author="user@gmail.com",
        last_commit="983466z",
        loc=1000,
        modified_date=datetime.fromisoformat("2019-08-01T05:00:00+00:00"),
        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        seen_at=datetime.fromisoformat("2018-08-01T05:00:00+00:00"),
        sorts_risk_level=100,
    )


@pytest.mark.changes_db
@freeze_time("2022-08-01T05:00:00+00:00")
async def test_update() -> None:
    group_name = "unittesting"
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    filename = "product/test/new#.new"
    loaders = get_new_context()
    current_value = await loaders.toe_lines.load(
        ToeLinesRequest(
            group_name=group_name, root_id=root_id, filename=filename
        )
    )
    attributes = ToeLinesAttributesToUpdate(
        attacked_at=datetime.fromisoformat("2021-08-01T05:00:00+00:00"),
        attacked_by="hacker2@test.com",
        attacked_lines=434,
        comments="comment test 2",
        last_author="customer2@gmail.com",
        has_vulnerabilities=False,
        loc=1111,
        last_commit="993466z",
        modified_date=datetime.fromisoformat("2020-08-01T05:00:00+00:00"),
        seen_at=datetime.fromisoformat("2019-08-01T05:00:00+00:00"),
        sorts_risk_level=50,
    )
    await toe_lines_domain.update(current_value, attributes)
    loaders = get_new_context()
    toe_lines = await loaders.toe_lines.load(
        ToeLinesRequest(
            group_name=group_name, root_id=root_id, filename=filename
        )
    )
    assert toe_lines == ToeLines(
        attacked_at=datetime.fromisoformat("2021-08-01T05:00:00+00:00"),
        attacked_by="hacker2@test.com",
        attacked_lines=434,
        be_present=True,
        be_present_until=None,
        comments="comment test 2",
        filename="product/test/new#.new",
        first_attack_at=datetime.fromisoformat("2020-08-01T05:00:00+00:00"),
        group_name="unittesting",
        has_vulnerabilities=False,
        last_author="customer2@gmail.com",
        last_commit="993466z",
        loc=1111,
        modified_date=datetime.fromisoformat("2020-08-01T05:00:00+00:00"),
        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        seen_at=datetime.fromisoformat("2019-08-01T05:00:00+00:00"),
        sorts_risk_level=50,
    )
