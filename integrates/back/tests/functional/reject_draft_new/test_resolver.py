from . import (
    get_result,
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
        ["admin@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
    ],
)
async def test_reject_draft(
    populate: bool, email: str, finding_id: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["rejectDraft"]
    assert result["data"]["rejectDraft"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reject_draft_new")
@pytest.mark.parametrize(
    ["email", "finding_id"],
    [
        ["hacker@gmail.com", "475041520"],
        ["customer@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
        ["executive@gmail.com", "475041520"],
    ],
)
async def test_reject_draft_fail(
    populate: bool, email: str, finding_id: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
