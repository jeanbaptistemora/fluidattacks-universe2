from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
)
from group_access import (
    domain as group_access_domain,
)
from names import (
    domain as names_domain,
)
from organizations import (
    domain as orgs_domain,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_group(populate: bool, email: str) -> None:
    assert populate
    org_name: str = "orgtest"
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email, org=org_name, group=group_name
    )
    assert "errors" not in result
    assert "success" in result["data"]["addGroup"]
    assert result["data"]["addGroup"]["success"]

    assert await names_domain.exists(group_name, "group") is False

    loaders: Dataloaders = get_new_context()
    group: Group = await loaders.group_typed.load(group_name)
    assert group.agent_token is None
    assert group.language == GroupLanguage.EN
    assert group.organization_name == org_name
    assert group.state.has_machine is True
    assert group.state.has_squad is True
    assert group.state.modified_by == email
    assert group.state.service == GroupService.WHITE
    assert group.state.status == GroupStateStatus.ACTIVE
    assert group.state.tier == GroupTier.FREE
    assert group.state.type == GroupSubscriptionType.CONTINUOUS

    org_id = await orgs_domain.get_id_by_name(org_name)
    org_groups: tuple[str, ...] = await orgs_domain.get_groups(org_id)
    assert group_name in org_groups
    assert await orgs_domain.has_user_access(org_id, email)
    # Admins are not granted access to the group
    group_users = await group_access_domain.get_group_users(group_name)
    assert email not in group_users


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group")
@pytest.mark.parametrize(
    ["email"],
    [
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["executive@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_group_fail(populate: bool, email: str) -> None:
    assert populate
    org_name: str = "orgtest"
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email, org=org_name, group=group_name
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
