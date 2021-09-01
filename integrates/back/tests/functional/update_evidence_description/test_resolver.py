from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_evidence_description")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["closer@gmail.com"],
    ],
)
async def test_update_evidence_description(populate: bool, email: str) -> None:
    assert populate
    draft_id: str = "475041513"
    draft_description: str = "this is a test description"
    evidence_name: str = "EVIDENCE1"
    result: Dict[str, Any] = await get_result(
        user=email,
        description=draft_description,
        draft=draft_id,
        evidence=evidence_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateEvidenceDescription"]
    assert result["data"]["updateEvidenceDescription"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_evidence_description")
@pytest.mark.parametrize(
    ["email"],
    [
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_update_evidence_description_fail(
    populate: bool, email: str
) -> None:
    assert populate
    draft_id: str = "475041513"
    draft_description: str = "this is a test description"
    evidence_name: str = "EVIDENCE1"
    result: Dict[str, Any] = await get_result(
        user=email,
        description=draft_description,
        draft=draft_id,
        evidence=evidence_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
