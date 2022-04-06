# pylint: disable=import-error
from . import (
    get_result_me_query,
    get_result_mutation,
    get_result_stakeholder_query,
)
from back.tests.functional.utils import (
    confirm_deletion,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.users.types import (
    NotificationsPreferences,
    User,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder")
@pytest.mark.parametrize(
    ["email", "role", "admin_email"],
    [
        [
            "customer_manager@fluidattacks.com",
            "customer_manager",
            "admin@gmail.com",
        ],
    ],
)
async def test_remove_stakeholder(
    populate: bool, email: str, role: str, admin_email: str
) -> None:
    assert populate
    group_name: str = "group1"
    organization_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result_me_query: Dict[str, Any] = await get_result_me_query(
        user=email, organization_id=organization_id
    )
    result_stakeholder_query: Dict[
        str, Any
    ] = await get_result_stakeholder_query(
        user=admin_email, stakeholder=email, group_name=group_name
    )
    result_organization_stakeholder_query: Dict[
        str, Any
    ] = await get_result_stakeholder_query(
        user=admin_email,
        stakeholder=email,
        group_name=group_name,
        organization_id=organization_id,
        entity="ORGANIZATION",
    )
    old_loaders: Dataloaders = get_new_context()
    old_user: User = await old_loaders.user.load(email)

    assert old_user.email == email
    assert "ACCESS_GRANTED" in old_user.notifications_preferences.email
    assert "DAILY_DIGEST" in old_user.notifications_preferences.email

    assert not result_me_query["data"]["me"]["remember"]
    assert result_me_query["data"]["me"]["role"] == role
    assert result_stakeholder_query["data"]["stakeholder"]["email"] == email
    assert result_stakeholder_query["data"]["stakeholder"]["role"] == role
    assert (
        len(
            result_organization_stakeholder_query["data"]["stakeholder"][
                "groups"
            ]
        )
        == 1
    )
    assert (
        result_stakeholder_query["data"]["stakeholder"]["responsibility"] == ""
    )

    result: Dict[str, Any] = await get_result_mutation(
        user=email,
    )
    assert "errors" not in result
    assert result["data"]["removeStakeholder"]["success"]

    await confirm_deletion(email=email)

    result_me_query = await get_result_me_query(
        user=email, organization_id=organization_id
    )
    result_stakeholder_query = await get_result_stakeholder_query(
        user=admin_email, stakeholder=email, group_name=group_name
    )
    assert "errors" in result_me_query
    assert "errors" in result_stakeholder_query
    assert result_me_query["errors"][0]["message"] == "Access denied"
    assert (
        result_stakeholder_query["errors"][0]["message"]
        == "Access denied or stakeholder not found"
    )

    result_organization_stakeholder_query = await get_result_stakeholder_query(
        user=admin_email,
        stakeholder=email,
        group_name=group_name,
        organization_id=organization_id,
        entity="ORGANIZATION",
    )
    assert "errors" in result_organization_stakeholder_query
    assert (
        result_organization_stakeholder_query["errors"][0]["message"]
        == "Access denied or stakeholder not found"
    )

    new_loaders: Dataloaders = get_new_context()
    new_user: User = await new_loaders.user.load(email)
    assert new_user.email == ""
    assert "ACCESS_GRANTED" not in new_user.notifications_preferences.email
    assert "DAILY_DIGEST" not in new_user.notifications_preferences.email
    assert new_user.notifications_preferences == NotificationsPreferences(
        email=[]
    )
