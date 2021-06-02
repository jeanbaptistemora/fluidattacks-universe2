from . import (
    query,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_draft_new")
@pytest.mark.parametrize(
    ["email", "finding_id"],
    [
        ["admin@gmail.com", "475041513"],
        ["analyst@gmail.com", "475041520"],
    ],
)
async def test_reject_draft(
    populate: bool, email: str, finding_id: str
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await query(
        user=email, finding_id=finding_id, group_name=group_name
    )
    assert "errors" not in result
    assert "success" in result["data"]["rejectDraft"]
    assert result["data"]["rejectDraft"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_draft_new")
@pytest.mark.parametrize(
    ["email", "finding_id"],
    [
        ["customer@gmail.com", "475041513"],
        ["executive@gmail.com", "475041520"],
    ],
)
async def test_reject_draft_fail(
    populate: bool, email: str, finding_id: str
) -> None:
    assert populate
    group_name: str = "group1"
    result: Dict[str, Any] = await query(
        user=email, finding_id=finding_id, group_name=group_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
