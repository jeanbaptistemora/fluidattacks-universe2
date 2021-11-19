from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_draft")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
    ],
)
async def test_add_draft(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    if email == "admin@gmail.com":
        assert "errors" not in result
        assert "success" in result["data"]["addDraft"]
        assert result["data"]["addDraft"]["success"]
    else:
        assert "errors" in result
        assert result["errors"][0]["message"] == (
            "Exception - A draft of this type has been already created."
            " Please submit vulnerabilities there"
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_draft")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_add_draft_fail(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
