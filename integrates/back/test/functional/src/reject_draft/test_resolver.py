from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_draft")
@pytest.mark.parametrize(
    ["email", "finding_id", "reasons"],
    [
        ["hacker@gmail.com", "475041520", "CONSISTENCY"],
        [
            "user@gmail.com",
            "3c475384-834c-47b0-ac71-a41a022e401c",
            "SCORING, CONSISTENCY",
        ],
        ["admin@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c", "OTHER"],
    ],
)
async def test_reject_draft_fail(
    populate: bool, email: str, finding_id: str, reasons: str
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        finding_id=finding_id,
        reasons=reasons,
    )
    assert "errors" in result
    if email == "admin@gmail.com":
        assert (
            result["errors"][0]["message"]
            == "Exception - This draft has missing fields: other"
        )
    else:
        assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_draft")
@pytest.mark.parametrize(
    ["email", "finding_id", "reasons"],
    [
        [
            "admin@gmail.com",
            "3c475384-834c-47b0-ac71-a41a022e401c",
            "WRITING, SCORING",
        ],
    ],
)
async def test_reject_draft(
    populate: bool,
    email: str,
    finding_id: str,
    reasons: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        finding_id=finding_id,
        reasons=reasons,
    )
    assert "errors" not in result
    assert "success" in result["data"]["rejectDraft"]
    assert result["data"]["rejectDraft"]["success"]
