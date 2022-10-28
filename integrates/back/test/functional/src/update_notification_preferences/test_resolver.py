# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderState,
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
    stakeholder: Stakeholder = await loaders.stakeholder.load(email)

    assert stakeholder.email == email
    assert "ACCESS_GRANTED" in stakeholder.notifications_preferences.email

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
    assert "ACCESS_GRANTED" not in stakeholder.notifications_preferences.email
    assert "REMEDIATE_FINDING" in stakeholder.notifications_preferences.email
    assert "REMEDIATE_FINDING" in stakeholder.notifications_preferences.sms
    assert "REMINDER_NOTIFICATION" in stakeholder.notifications_preferences.sms
    assert (
        stakeholder.notifications_preferences.parameters.min_severity
        == Decimal("6.7")
    )
    assert stakeholder.state is not None
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
    historic_state: tuple[StakeholderState, ...] = await get_historic_state(
        email=email
    )
    assert stakeholder.state == historic_state[-1]
