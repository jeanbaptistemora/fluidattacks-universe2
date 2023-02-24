from . import (
    get_result,
    query_get,
)
from _pytest.monkeypatch import (
    MonkeyPatch,
)
import asyncio
from freezegun import (
    freeze_time,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("refresh_toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
@freeze_time("2021-11-10T20:35:20.372236+00:00")
async def test_refresh_toe_lines(
    populate: bool, email: str, monkeypatch: MonkeyPatch
) -> None:
    assert populate
    group_name = "group1"
    result: dict[str, Any] = await get_result(
        user=email, group_name=group_name, monkeypatch=monkeypatch
    )
    await asyncio.sleep(8)

    assert result["data"]["refreshToeLines"]["success"]
    result = await query_get(user=email, group_name=group_name)
    lines = result["data"]["group"]["toeLines"]["edges"]
    assert lines[0]["node"]["attackedAt"] is None
    assert lines[0]["node"]["attackedBy"] == ""
    assert lines[0]["node"]["attackedLines"] == 0
    assert lines[0]["node"]["bePresent"] is True
    assert lines[0]["node"]["bePresentUntil"] is None
    assert lines[0]["node"]["comments"] == ""
    assert lines[0]["node"]["filename"] == "test5/test.sh"
    assert lines[0]["node"]["firstAttackAt"] is None
    assert lines[0]["node"]["lastAuthor"] == "authoremail@test.com"
    assert (
        lines[0]["node"]["lastCommit"]
        == "50a516954a321f95c6fb8baccb640e87d2f5d193"
    )
    assert lines[0]["node"]["loc"] == 3
    assert lines[0]["node"]["modifiedDate"] == "2021-11-11T17:41:46+00:00"
    assert lines[0]["node"]["seenAt"] == "2021-11-10T20:35:20.372236+00:00"
    assert lines[0]["node"]["sortsRiskLevel"] == -1


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("refresh_toe_lines")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["service_forces@fluidattacks.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_refresh_toe_lines_fail(
    populate: bool, email: str, monkeypatch: MonkeyPatch
) -> None:
    assert populate
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, group_name="group1", monkeypatch=monkeypatch
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
