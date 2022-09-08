# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_query,
    put_mutation,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("subscribe_to_entity_report")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_subscribe_to_entity_report(populate: bool, email: str) -> None:
    assert populate
    organization_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result_mutation = await put_mutation(
        entity=SubscriptionEntity.ORGANIZATION,
        email=email,
        frequency=SubscriptionFrequency.MONTHLY,
        subject=organization_id,
    )
    assert "errors" not in result_mutation
    assert result_mutation["data"]["subscribeToEntityReport"]["success"]

    group_name = "group1"
    result_mutation = await put_mutation(
        entity=SubscriptionEntity.GROUP,
        email=email,
        frequency=SubscriptionFrequency.WEEKLY,
        subject=group_name,
    )
    assert "errors" not in result_mutation
    assert result_mutation["data"]["subscribeToEntityReport"]["success"]

    expected_subscriptions: list[dict[str, str]] = [
        {
            "entity": "GROUP",
            "frequency": "WEEKLY",
            "subject": group_name,
        },
        {
            "entity": "ORGANIZATION",
            "frequency": "MONTHLY",
            "subject": organization_id,
        },
    ]
    result_query = await get_query(
        email=email,
    )
    assert (
        result_query["data"]["me"]["subscriptionsToEntityReport"]
        == expected_subscriptions
    )

    result_mutation = await put_mutation(
        entity=SubscriptionEntity.GROUP,
        email=email,
        frequency=SubscriptionFrequency.NEVER,
        subject=group_name,
    )
    assert "errors" not in result_mutation
    assert result_mutation["data"]["subscribeToEntityReport"]["success"]

    result_query = await get_query(
        email=email,
    )
    assert (
        result_query["data"]["me"]["subscriptionsToEntityReport"]
        == expected_subscriptions[-1:]
    )
