from . import (
    get_query,
    put_mutation,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from db_model.subscriptions.types import (
    Subscription,
    SubscriptionState,
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
    expected_subscriptions[0]["frequency"] = "NEVER"
    assert (
        result_query["data"]["me"]["subscriptionsToEntityReport"]
        == expected_subscriptions
    )

    expected_historical_subscription: tuple[Subscription, Subscription] = (
        Subscription(
            email=email,
            entity=SubscriptionEntity.GROUP,
            subject=group_name,
            frequency=SubscriptionFrequency.WEEKLY,
            state=SubscriptionState(modified_date=None),
        ),
        Subscription(
            email=email,
            entity=SubscriptionEntity.GROUP,
            subject=group_name,
            frequency=SubscriptionFrequency.NEVER,
            state=SubscriptionState(modified_date=None),
        ),
    )
    loaders: Dataloaders = get_new_context()
    group_historic_subscriptions = (
        await loaders.stakeholder_historic_subscription.load(
            (email, SubscriptionEntity.GROUP, group_name)
        )
    )
    assert (
        len(expected_historical_subscription)
        == len(group_historic_subscriptions)
        == 2
    )
    for expected_sub, actual_sub in zip(
        expected_historical_subscription, group_historic_subscriptions
    ):
        assert expected_sub.email == actual_sub.email
        assert expected_sub.entity == actual_sub.entity
        assert expected_sub.subject == actual_sub.subject
        assert expected_sub.frequency == actual_sub.frequency
        assert actual_sub.state.modified_date
