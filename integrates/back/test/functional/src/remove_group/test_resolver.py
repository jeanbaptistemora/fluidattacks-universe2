from . import (
    get_query_group,
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.enums import (
    GroupStateJustification,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_group(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        comments="This is a dummy explanation for the removal.",
        email=email,
        group=group_name,
        reason=GroupStateJustification.NO_SYSTEM,
    )
    assert "errors" not in result
    assert result["data"]["removeGroup"]["success"]

    query_result = await get_query_group(email=email, group_name=group_name)
    assert "errors" in query_result
    assert (
        query_result["errors"][0]["message"]
        == "Access denied or group not found"
    )

    loaders: Dataloaders = get_new_context()
    findings: tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    assert not findings


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_remove_group_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group2"
    result: dict[str, Any] = await get_result(
        comments="",
        email=email,
        group=group_name,
        reason=GroupStateJustification.NO_SYSTEM,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
