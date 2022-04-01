from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.constants import (
    MASKED,
)
from db_model.groups.enums import (
    GroupService,
    GroupStateRemovalJustification,
    GroupStateStatus,
    GroupTier,
)
from db_model.groups.types import (
    Group,
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
        user=email,
        group=group_name,
        reason=GroupStateRemovalJustification.NO_SYSTEM.value,
    )
    assert "errors" not in result
    assert result["data"]["removeGroup"]["success"]

    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group_typed.load(group_name)
    assert group.state.has_machine is False
    assert group.state.has_squad is False
    assert (
        group.state.justification == GroupStateRemovalJustification.NO_SYSTEM
    )
    assert group.state.modified_by == email
    assert group.state.service == GroupService.WHITE
    assert group.state.status == GroupStateStatus.DELETED
    assert group.state.tier == GroupTier.FREE
    for file in group.files:
        assert file.description == MASKED
        assert file.file_name == MASKED
        assert file.modified_by == MASKED
        assert file.modified_date
        assert file.modified_date != MASKED

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
        ["executive@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_remove_group_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group2"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
        reason=GroupStateRemovalJustification.NO_SYSTEM.value,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
