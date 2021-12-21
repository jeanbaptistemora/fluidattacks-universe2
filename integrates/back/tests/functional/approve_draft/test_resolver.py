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
    ["email", "finding_id"],
    [
        ["admin@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
        ["reviewer@gmail.com", "475041520"],
    ],
)
async def test_approve_draft(
    populate: bool, email: str, finding_id: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["approveDraft"]
    assert result["data"]["approveDraft"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("approve_draft")
@pytest.mark.parametrize(
    ["email", "finding_id"],
    [
        ["hacker@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
        ["reattacker@gmail.com", "3c475384-834c-47b0-ac71-a41a022e401c"],
        ["executive@gmail.com", "475041520"],
    ],
)
async def test_approve_draft_fail(
    populate: bool, email: str, finding_id: str
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email, finding_id=finding_id
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
