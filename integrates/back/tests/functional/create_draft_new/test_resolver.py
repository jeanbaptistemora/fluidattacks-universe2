# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("create_draft_new")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["analyst@gmail.com"],
    ],
)
async def test_create_draft(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
    )
    assert "errors" not in result
    assert "success" in result["data"]["createDraft"]
    assert result["data"]["createDraft"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("create_draft_new")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_create_draft_fail(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
