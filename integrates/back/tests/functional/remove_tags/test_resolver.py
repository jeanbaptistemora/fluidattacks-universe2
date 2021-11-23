from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tags")
async def test_remove_single_tag(populate: bool) -> None:
    assert populate
    user_email = "hacker@gmail.com"
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vuln_id: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    tag_to_remove = "tag3"

    loaders: Dataloaders = get_new_context()
    vuln: Vulnerability = await loaders.vulnerability_typed.load(vuln_id)
    assert vuln.tags == ["tag1", "tag2", "tag3"]

    result: Dict[str, Any] = await get_result(
        user=user_email,
        finding=finding_id,
        vuln_id=vuln_id,
        tag=tag_to_remove,
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeTags"]
    assert result["data"]["removeTags"]["success"]

    loaders.vulnerability_typed.clear(vuln_id)
    vuln = await loaders.vulnerability_typed.load(vuln_id)
    assert vuln.tags == ["tag1", "tag2"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tags")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["customer@gmail.com"],
        ["customeradmin@gmail.com"],
        ["executive@gmail.com"],
        ["system_owner@gmail.com"],
    ],
)
async def test_remove_all_tags(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vuln_id: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vuln_id=vuln_id
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeTags"]
    assert result["data"]["removeTags"]["success"]

    loaders: Dataloaders = get_new_context()
    vuln: Vulnerability = await loaders.vulnerability_typed.load(vuln_id)
    assert vuln.tags == None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_tags")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["reattacker@gmail.com"],
    ],
)
async def test_remove_tags_fail(populate: bool, email: str) -> None:
    assert populate
    finding_id: str = "3c475384-834c-47b0-ac71-a41a022e401c"
    vuln_uuid: str = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
    result: Dict[str, Any] = await get_result(
        user=email, finding=finding_id, vuln_id=vuln_uuid
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
