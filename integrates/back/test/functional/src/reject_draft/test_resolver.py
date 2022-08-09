from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_draft")
@pytest.mark.parametrize(
    ["email", "finding_id", "reason"],
    [
        ["hacker@gmail.com", "475041520", "CONSISTENCY"],
        ["user@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c", "SCORING"],
        ["admin@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c", "OTHER"],
    ],
)
async def test_reject_draft_fail(
    populate: bool, email: str, finding_id: str, reason: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        finding_id=finding_id,
        reason=reason,
    )
    assert "errors" in result
    if email == "admin@gmail.com":
        assert (
            result["errors"][0]["message"]
            == "Exception - This draft has missing fields: reason"
        )
    else:
        assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_draft")
@pytest.mark.parametrize(
    ["email", "finding_id", "reason"],
    [
        ["admin@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c", "WRITING"],
    ],
)
async def test_reject_draft(
    populate: bool,
    email: str,
    finding_id: str,
    reason: str,
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        finding_id=finding_id,
        reason=reason,
    )
    assert "errors" not in result
    assert "success" in result["data"]["rejectDraft"]
    assert result["data"]["rejectDraft"]["success"]
