from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("submit_draft_new")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_submit_draft(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "475041513"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id, group_name=group_name
    )
    assert "errors" not in result
    assert result["data"]["submitDraft"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("submit_draft_new")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
    ],
)
async def test_submit_draft_fail_1(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "475041513"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id, group_name=group_name
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - This draft has already been submitted"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("submit_draft_new")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_submit_draft_fail_2(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "475041513"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id, group_name=group_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
