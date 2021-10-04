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
@pytest.mark.resolver_test_group("update_severity")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
    ],
)
async def test_update_severity(populate: bool, email: str) -> None:
    assert populate
    draft_id: str = "475041513"
    result: Dict[str, Any] = await get_result(user=email, draft=draft_id)
    assert "errors" not in result
    assert "success" in result["data"]["updateSeverity"]
    assert result["data"]["updateSeverity"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_severity")
@pytest.mark.parametrize(
    ["email"],
    [
        ["reattacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_update_severity_fail(populate: bool, email: str) -> None:
    assert populate
    draft_id: str = "475041513"
    result: Dict[str, Any] = await get_result(user=email, draft=draft_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
