from . import (
    query,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
    ],
)
async def test_upload_file(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "475041513"
    result: Dict[str, Any] = await query(user=email, finding=finding_id)
    assert "errors" not in result
    assert result["data"]["uploadFile"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["executive@gmail.com"],
    ],
)
async def test_upload_file_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "475041513"
    result: Dict[str, Any] = await query(user=email, finding=finding_id)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
