from dataloaders import (
    get_new_context,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    RootToeLinesRequest,
    ToeLines,
    ToeLinesConnection,
    ToeLinesEdge,
    ToeLinesRequest,
)
from dynamodb.types import (
    PageInfo,
)
import pytest

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    filename = "test/test#.config"
    toe_lines = await loaders.toe_lines.load(
        ToeLinesRequest(
            group_name=group_name, root_id=root_id, filename=filename
        )
    )
    assert toe_lines == ToeLines(
        attacked_at="2021-02-20T05:00:00+00:00",
        attacked_by="test2@test.com",
        attacked_lines=4,
        be_present=True,
        be_present_until="",
        comments="comment 1",
        commit_author="customer@gmail.com",
        filename="test/test#.config",
        first_attack_at="2020-02-19T15:41:04+00:00",
        group_name="unittesting",
        loc=8,
        modified_commit="983466z",
        modified_date="2020-11-15T15:41:04+00:00",
        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        seen_at="2020-02-01T15:41:04+00:00",
        sorts_risk_level=80,
    )
    group_name = "unittesting"
    root_id = "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
    filename = "test2/test.sh"
    toe_lines = await loaders.toe_lines.load(
        ToeLinesRequest(
            group_name=group_name, root_id=root_id, filename=filename
        )
    )
    assert toe_lines == ToeLines(
        attacked_at="2021-01-20T05:00:00+00:00",
        attacked_by="test@test.com",
        attacked_lines=120,
        be_present=False,
        be_present_until="2021-01-01T15:41:04+00:00",
        comments="comment 2",
        commit_author="customer@gmail.com",
        filename="test2/test.sh",
        first_attack_at="2020-01-19T15:41:04+00:00",
        group_name="unittesting",
        loc=172,
        modified_commit="273412t",
        modified_date="2020-11-16T15:41:04+00:00",
        root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
        seen_at="2020-01-01T15:41:04+00:00",
        sorts_risk_level=0,
    )


async def test_get_by_group() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load(
        GroupToeLinesRequest(group_name=group_name)
    )
    assert group_toe_lines == ToeLinesConnection(
        edges=(
            ToeLinesEdge(
                node=ToeLines(
                    attacked_at="2021-02-20T05:00:00+00:00",
                    attacked_by="test2@test.com",
                    attacked_lines=4,
                    be_present=True,
                    be_present_until="",
                    comments="comment 1",
                    commit_author="customer@gmail.com",
                    filename="test/test#.config",
                    first_attack_at="2020-02-19T15:41:04+00:00",
                    group_name="unittesting",
                    loc=8,
                    modified_commit="983466z",
                    modified_date="2020-11-15T15:41:04+00:00",
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    seen_at="2020-02-01T15:41:04+00:00",
                    sorts_risk_level=80,
                ),
                cursor="eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJMSU5FUyNST09UIzQwMzlkMDk4LWZmYzUtNDk4NC04ZWQzLWViMTdiY2E5OGUxOSNGSUxFTkFNRSN0ZXN0L3Rlc3QjLmNvbmZpZyJ9",
            ),
            ToeLinesEdge(
                node=ToeLines(
                    attacked_at="2021-01-20T05:00:00+00:00",
                    attacked_by="test@test.com",
                    attacked_lines=120,
                    be_present=False,
                    be_present_until="2021-01-01T15:41:04+00:00",
                    comments="comment 2",
                    commit_author="customer@gmail.com",
                    filename="test2/test.sh",
                    first_attack_at="2020-01-19T15:41:04+00:00",
                    group_name="unittesting",
                    loc=172,
                    modified_commit="273412t",
                    modified_date="2020-11-16T15:41:04+00:00",
                    root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    seen_at="2020-01-01T15:41:04+00:00",
                    sorts_risk_level=0,
                ),
                cursor="eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJMSU5FUyNST09UIzc2NWIxZDBmLWI2ZmItNDQ4NS1iNGUyLTJjMmNiMTU1NWIxYSNGSUxFTkFNRSN0ZXN0Mi90ZXN0LnNoIn0=",
            ),
        ),
        page_info=PageInfo(has_next_page=False, end_cursor="bnVsbA=="),
    )


async def test_get_by_root() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    root_toe_lines = await loaders.root_toe_lines.load(
        RootToeLinesRequest(group_name=group_name, root_id=root_id)
    )
    assert root_toe_lines == ToeLinesConnection(
        edges=(
            ToeLinesEdge(
                node=ToeLines(
                    attacked_at="2021-02-20T05:00:00+00:00",
                    attacked_by="test2@test.com",
                    attacked_lines=4,
                    be_present=True,
                    be_present_until="",
                    comments="comment 1",
                    commit_author="customer@gmail.com",
                    filename="test/test#.config",
                    first_attack_at="2020-02-19T15:41:04+00:00",
                    group_name="unittesting",
                    loc=8,
                    modified_commit="983466z",
                    modified_date="2020-11-15T15:41:04+00:00",
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    seen_at="2020-02-01T15:41:04+00:00",
                    sorts_risk_level=80,
                ),
                cursor="eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJMSU5FUyNST09UIzQwMzlkMDk4LWZmYzUtNDk4NC04ZWQzLWViMTdiY2E5OGUxOSNGSUxFTkFNRSN0ZXN0L3Rlc3QjLmNvbmZpZyJ9",
            ),
        ),
        page_info=PageInfo(has_next_page=False, end_cursor="bnVsbA=="),
    )
    group_name = "unittesting"
    root_id = "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
    root_toe_lines = await loaders.root_toe_lines.load(
        RootToeLinesRequest(group_name=group_name, root_id=root_id)
    )
    assert root_toe_lines == ToeLinesConnection(
        edges=(
            ToeLinesEdge(
                node=ToeLines(
                    attacked_at="2021-01-20T05:00:00+00:00",
                    attacked_by="test@test.com",
                    attacked_lines=120,
                    be_present=False,
                    be_present_until="2021-01-01T15:41:04+00:00",
                    comments="comment 2",
                    commit_author="customer@gmail.com",
                    filename="test2/test.sh",
                    first_attack_at="2020-01-19T15:41:04+00:00",
                    group_name="unittesting",
                    loc=172,
                    modified_commit="273412t",
                    modified_date="2020-11-16T15:41:04+00:00",
                    root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    seen_at="2020-01-01T15:41:04+00:00",
                    sorts_risk_level=0,
                ),
                cursor="eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJMSU5FUyNST09UIzc2NWIxZDBmLWI2ZmItNDQ4NS1iNGUyLTJjMmNiMTU1NWIxYSNGSUxFTkFNRSN0ZXN0Mi90ZXN0LnNoIn0=",
            ),
        ),
        page_info=PageInfo(has_next_page=False, end_cursor="bnVsbA=="),
    )
