from . import (
    get_result,
    query_get,
)
from custom_exceptions import (
    InvalidSortsRiskLevel,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest.mark.parametrize(("sorts_risk_level"), ((0), (10), (100)))
@pytest.mark.parametrize(
    ("sorts_risk_level_date"),
    (
        ("2021-01-20"),
        ("2021-02-20"),
        ("2021-03-20"),
    ),
)
@pytest.mark.parametrize(
    ("sorts_suggestions"),
    (
        (
            [
                {
                    "findingTitle": "014. Insecure functionality",
                    "probability": 55,
                },
                {
                    "findingTitle": "007. Cross-site request forgery",
                    "probability": 44,
                },
                {
                    "findingTitle": "083. XML injection (XXE)",
                    "probability": 0,
                },
            ]
        ),
    ),
)
async def test_update_toe_lines_sorts(
    populate: bool,
    sorts_risk_level: int,
    sorts_risk_level_date: str,
    sorts_suggestions: list[dict[str, Any]],
) -> None:
    assert populate
    user_email = "admin@fluidattacks.com"
    result: dict[str, Any] = await get_result(
        user=user_email,
        group_name="group1",
        root_nickname="asm_1",
        filename="test2/test.sh",
        sorts_risk_level=sorts_risk_level,
        sorts_risk_level_date=sorts_risk_level_date,
        sorts_suggestions=sorts_suggestions,
    )
    assert result["data"]["updateToeLinesSorts"]["success"]
    result = await query_get(user=user_email, group_name="group1")
    lines = result["data"]["group"]["toeLines"]["edges"]
    assert lines[0]["node"]["attackedAt"] == "2021-01-20T05:00:00+00:00"
    assert lines[0]["node"]["attackedBy"] == "test@test.com"
    assert lines[0]["node"]["attackedLines"] == 23
    assert lines[0]["node"]["bePresent"] is False
    assert lines[0]["node"]["bePresentUntil"] == "2021-01-19T15:41:04+00:00"
    assert lines[0]["node"]["comments"] == "comment 1"
    assert lines[0]["node"]["filename"] == "test/test#.config"
    assert lines[0]["node"]["firstAttackAt"] == "2020-01-19T15:41:04+00:00"
    assert lines[0]["node"]["lastAuthor"] == "customer1@gmail.com"
    assert (
        lines[0]["node"]["lastCommit"]
        == "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1"
    )
    assert lines[0]["node"]["loc"] == 4324
    assert lines[0]["node"]["modifiedDate"] == "2020-11-16T15:41:04+00:00"
    assert lines[0]["node"]["root"]["nickname"] == "universe"
    assert lines[0]["node"]["seenAt"] == "2020-01-01T15:41:04+00:00"
    assert lines[0]["node"]["sortsRiskLevel"] == 0


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest.mark.parametrize(("sorts_risk_level"), ((-10), (-1), (101), (1000)))
async def test_update_toe_lines_sorts_range_fail(
    populate: bool, sorts_risk_level: int
) -> None:
    assert populate
    user_email = "admin@fluidattacks.com"
    result: dict[str, Any] = await get_result(
        user=user_email,
        group_name="group1",
        root_nickname="asm_1",
        filename="test2/test.sh",
        sorts_risk_level=sorts_risk_level,
        sorts_risk_level_date="2021-01-20",
        sorts_suggestions=[],
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == InvalidSortsRiskLevel.msg


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
async def test_update_toe_lines_sorts_no_filename(populate: bool) -> None:
    assert populate
    user_email = "admin@fluidattacks.com"
    result: dict[str, Any] = await get_result(
        user=user_email,
        group_name="group1",
        root_nickname="asm_1",
        filename="non_existing_filename",
        sorts_risk_level=10,
        sorts_risk_level_date="2021-01-20",
        sorts_suggestions=[],
    )
    assert (
        result["errors"][0]["message"]
        == "Exception - Toe lines has not been found"
    )
