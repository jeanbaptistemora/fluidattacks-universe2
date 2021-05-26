# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_evidence(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        finding="475041513",
        evidence="EVIDENCE1",
    )
    assert "errors" not in result
    assert result["data"]["removeEvidence"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["analyst@gmail.com"],
        ["closer@gmail.com"],
    ],
)
async def test_remove_evidence_fail_1(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        finding="475041513",
        evidence="EVIDENCE1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Exception - Evidence not found"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_evidence")
@pytest.mark.parametrize(
    ["email"],
    [
        ["executive@gmail.com"],
    ],
)
async def test_remove_evidence_fail_2(populate: bool, email: str) -> None:
    assert populate
    result: Dict[str, Any] = await query(
        user=email,
        finding="475041513",
        evidence="EVIDENCE1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
