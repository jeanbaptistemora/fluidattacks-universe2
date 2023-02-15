# pylint: disable=import-error
from . import (
    get_result_me_query,
    get_result_mutation,
    get_result_stakeholder_query,
)
from back.test.functional.src.organization import (
    get_result as get_organization_query,
)
from back.test.functional.src.update_notification_preferences import (
    get_result_mutation as put_update_notification_preferences,
)
from back.test.functional.src.utils import (
    confirm_deletion,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.stakeholders.get import (
    get_historic_state,
)
from decimal import (
    Decimal,
)
from organizations.domain import (
    EMAIL_INTEGRATES,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder")
@pytest.mark.parametrize(
    ["email", "admin_email"],
    [
        [
            "customer_manager@fluidattacks.com",
            "admin@gmail.com",
        ],
    ],
)
async def test_remove_stakeholder(
    populate: bool, email: str, admin_email: str
) -> None:
    assert populate
    group_name: str = "group1"
    organization_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result_me_query = await get_result_me_query(
        user=email, organization_id=organization_id
    )
    result_stakeholder_query = await get_result_stakeholder_query(
        user=admin_email, stakeholder=email, group_name=group_name
    )
    result_organization_stakeholder_query = await get_result_stakeholder_query(
        user=admin_email,
        stakeholder=email,
        group_name=group_name,
        organization_id=organization_id,
        entity="ORGANIZATION",
    )
    result_organization_query = await get_organization_query(
        user=admin_email,
        org=organization_id,
    )

    result = await put_update_notification_preferences(
        user=email,
        mail=["REMEDIATE_FINDING"],
        severity=Decimal("6.7"),
        sms=["REMINDER_NOTIFICATION", "REMEDIATE_FINDING"],
    )
    assert "errors" not in result
    assert result["data"]["updateNotificationsPreferences"]["success"]
    old_loaders: Dataloaders = get_new_context()
    old_stakeholder = await old_loaders.stakeholder.load(email)
    historic_state = await get_historic_state(email=email)
    assert old_stakeholder
    assert old_stakeholder.email == email
    assert old_stakeholder.state is not None
    assert (
        "REMEDIATE_FINDING"
        in old_stakeholder.state.notifications_preferences.email
    )
    assert old_stakeholder.state == historic_state[-1]

    assert not result_me_query["data"]["me"]["remember"]
    assert result_me_query["data"]["me"]["role"] == "user"
    assert result_stakeholder_query["data"]["stakeholder"]["email"] == email
    assert (
        result_stakeholder_query["data"]["stakeholder"]["role"]
        == "customer_manager"
    )
    assert (
        len(
            result_organization_stakeholder_query["data"]["stakeholder"][
                "groups"
            ]
        )
        == 1
    )
    assert (
        result_stakeholder_query["data"]["stakeholder"]["responsibility"]
        is None
    )
    len_organization_stakeholders = len(
        result_organization_query["data"]["organization"]["stakeholders"]
    )
    assert len_organization_stakeholders > 1
    assert (
        len(result_organization_query["data"]["organization"]["credentials"])
        == 1
    )
    assert (
        result_organization_query["data"]["organization"]["credentials"][0][
            "name"
        ]
        == "cred_https_token"
    )
    assert (
        result_organization_query["data"]["organization"]["credentials"][0][
            "owner"
        ]
        == email
    )

    result = await get_result_mutation(
        user=email,
    )
    assert "errors" not in result
    assert result["data"]["removeStakeholder"]["success"]

    await confirm_deletion(loaders=get_new_context(), email=email)

    new_loaders: Dataloaders = get_new_context()
    assert not await new_loaders.stakeholder.load(email)

    historic_state = await get_historic_state(email=email)
    assert len(historic_state) == 0

    result_stakeholder_query = await get_result_stakeholder_query(
        user=admin_email, stakeholder=email, group_name=group_name
    )
    assert "errors" in result_stakeholder_query
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

    result_organization_query = await get_organization_query(
        user=admin_email,
        org=organization_id,
    )
    assert (
        len(result_organization_query["data"]["organization"]["stakeholders"])
        == len_organization_stakeholders - 1
    )
    assert (
        result_organization_query["data"]["organization"]["credentials"][0][
            "name"
        ]
        == "cred_https_token"
    )
    assert (
        result_organization_query["data"]["organization"]["credentials"][0][
            "owner"
        ]
        == EMAIL_INTEGRATES
    )
