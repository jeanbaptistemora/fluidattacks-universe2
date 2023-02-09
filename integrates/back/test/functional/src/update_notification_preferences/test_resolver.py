from . import (
    get_result_mutation,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.stakeholders import (
    get_historic_state,
)
from decimal import (
    Decimal,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_notification_preferences")
@pytest.mark.parametrize(
    ["email"],
    [
        [
            "customer_manager@fluidattacks.com",
        ],
    ],
)
async def test_update_notification_preferences(
    populate: bool, email: str
) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder
    assert stakeholder.email == email
    assert (
        "ACCESS_GRANTED" in stakeholder.state.notifications_preferences.email
    )

    result = await get_result_mutation(
        user=email,
        mail=["REMEDIATE_FINDING"],
        severity=Decimal("6.7"),
        sms=["REMINDER_NOTIFICATION", "REMEDIATE_FINDING"],
    )
    assert "errors" not in result
    assert result["data"]["updateNotificationsPreferences"]["success"]

    loaders.stakeholder.clear_all()
    stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder
    assert (
        "ACCESS_GRANTED"
        not in stakeholder.state.notifications_preferences.email
    )
    assert (
        "REMEDIATE_FINDING"
        in stakeholder.state.notifications_preferences.email
    )
    assert (
        "REMEDIATE_FINDING" in stakeholder.state.notifications_preferences.sms
    )
    assert (
        "REMINDER_NOTIFICATION"
        in stakeholder.state.notifications_preferences.sms
    )
    assert (
        stakeholder.state.notifications_preferences.parameters.min_severity
        == Decimal("6.7")
    )
    historic_state = await get_historic_state(email=email)
    assert stakeholder.state == historic_state[-1]
