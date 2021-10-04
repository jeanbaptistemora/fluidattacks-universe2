from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.skip(reason="Temporarily disabled due to db migration")
@pytest.mark.asyncio
@pytest.mark.resolver_test_group("approve_draft")
@pytest.mark.parametrize(
    ("email", "draft_id"),
    (
        ("admin@gmail.com", "475041513"),
        ("reviewer@gmail.com", "475041514"),
    ),
)
async def test_approve_draft(
    populate: bool, email: str, draft_id: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        draft=draft_id,
    )
    assert "errors" not in result
    assert "success" in result["data"]["approveDraft"]
    assert result["data"]["approveDraft"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("approve_draft")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
    ],
)
async def test_approve_draft_fail(populate: bool, email: str) -> None:
    assert populate
    draft_id: str = "475041513"
    result: Dict[str, Any] = await get_result(
        user=email,
        draft=draft_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
