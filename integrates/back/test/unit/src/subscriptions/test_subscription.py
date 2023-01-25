from context import (
    FI_INTEGRATES_REPORTS_LOGO_PATH,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.subscriptions import (
    add,
    get_all_subscriptions,
    remove,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from db_model.subscriptions.types import (
    Subscription,
    SubscriptionState,
)
from newutils.subscriptions import (
    translate_entity,
)
import os
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


def test_image_path() -> None:
    assert os.path.exists(FI_INTEGRATES_REPORTS_LOGO_PATH)


def test_translate_entity() -> None:
    entity_org = SubscriptionEntity.ORGANIZATION
    assert translate_entity(entity=entity_org) == "org"
    entity_group = SubscriptionEntity.GROUP
    assert translate_entity(entity=entity_group) == "group"
    entity_portfolio = SubscriptionEntity.PORTFOLIO
    assert translate_entity(entity=entity_portfolio) == "portfolio"


@pytest.mark.changes_db
async def test_update() -> None:
    test_data_1 = Subscription(
        email="test_user_email@test.com",
        entity=SubscriptionEntity.ORGANIZATION,
        frequency=SubscriptionFrequency.WEEKLY,
        subject="test_report_subject",
        state=SubscriptionState(
            modified_date=datetime.fromisoformat("2022-10-27T20:07:57+00:00")
        ),
    )
    test_data_2 = Subscription(
        email="test_user_email2@test.com",
        entity=SubscriptionEntity.GROUP,
        frequency=SubscriptionFrequency.MONTHLY,
        subject="test_report_subject2",
        state=SubscriptionState(
            modified_date=datetime.fromisoformat("2022-10-27T20:07:57+00:00")
        ),
    )
    await add(subscription=test_data_1)
    await add(subscription=test_data_2)

    assert await get_all_subscriptions(
        frequency=SubscriptionFrequency.HOURLY
    ) == [
        Subscription(
            email="integratesmanager@gmail.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.HOURLY,
            subject="unittesting",
            state=SubscriptionState(
                modified_date=datetime.fromisoformat(
                    "2022-02-22T20:07:57+00:00"
                )
            ),
        ),
    ]
    assert await get_all_subscriptions(
        frequency=SubscriptionFrequency.DAILY
    ) == [
        Subscription(
            email="integratesmanager@fluidattacks.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.DAILY,
            subject="unittesting",
            state=SubscriptionState(
                modified_date=datetime.fromisoformat(
                    "2022-05-22T20:07:57+00:00"
                )
            ),
        ),
    ]
    assert await get_all_subscriptions(
        frequency=SubscriptionFrequency.WEEKLY
    ) == [
        Subscription(
            email="test_user_email@test.com",
            entity=SubscriptionEntity.ORGANIZATION,
            frequency=SubscriptionFrequency.WEEKLY,
            subject="test_report_subject",
            state=SubscriptionState(
                modified_date=datetime.fromisoformat(
                    "2022-10-27T20:07:57+00:00"
                )
            ),
        ),
    ]
    assert await get_all_subscriptions(
        frequency=SubscriptionFrequency.MONTHLY
    ) == [
        Subscription(
            email="integratesmanager@fluidattacks.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.MONTHLY,
            subject="oneshottest",
            state=SubscriptionState(
                modified_date=datetime.fromisoformat(
                    "2022-03-22T20:07:57+00:00"
                )
            ),
        ),
        Subscription(
            email="test_user_email2@test.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.MONTHLY,
            subject="test_report_subject2",
            state=SubscriptionState(
                modified_date=datetime.fromisoformat(
                    "2022-10-27T20:07:57+00:00"
                )
            ),
        ),
    ]

    loaders = get_new_context()

    assert await loaders.stakeholder_subscriptions.load(test_data_1.email) == [
        Subscription(
            email="test_user_email@test.com",
            entity=SubscriptionEntity.ORGANIZATION,
            frequency=SubscriptionFrequency.WEEKLY,
            subject="test_report_subject",
            state=SubscriptionState(
                modified_date=datetime.fromisoformat(
                    "2022-10-27T20:07:57+00:00"
                )
            ),
        )
    ]
    assert await loaders.stakeholder_subscriptions.load(test_data_2.email) == [
        Subscription(
            email="test_user_email2@test.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.MONTHLY,
            subject="test_report_subject2",
            state=SubscriptionState(
                modified_date=datetime.fromisoformat(
                    "2022-10-27T20:07:57+00:00"
                )
            ),
        )
    ]
    assert await loaders.stakeholder_subscriptions.load(
        "integratesmanager@gmail.com",
    ) == [
        Subscription(
            email="integratesmanager@gmail.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.HOURLY,
            subject="unittesting",
            state=SubscriptionState(
                modified_date=datetime.fromisoformat(
                    "2022-02-22T20:07:57+00:00"
                )
            ),
        )
    ]
    assert await loaders.stakeholder_subscriptions.load(
        "integratesmanager@fluidattacks.com",
    ) == [
        Subscription(
            email="integratesmanager@fluidattacks.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.MONTHLY,
            subject="oneshottest",
            state=SubscriptionState(
                modified_date=datetime.fromisoformat(
                    "2022-03-22T20:07:57+00:00"
                )
            ),
        ),
        Subscription(
            email="integratesmanager@fluidattacks.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.DAILY,
            subject="unittesting",
            state=SubscriptionState(
                modified_date=datetime.fromisoformat(
                    "2022-05-22T20:07:57+00:00"
                )
            ),
        ),
    ]


@pytest.mark.changes_db
async def test_historic_sub_add_and_delete() -> None:
    test_data_1 = Subscription(
        email="test_user_email@test.com",
        entity=SubscriptionEntity.ORGANIZATION,
        frequency=SubscriptionFrequency.WEEKLY,
        subject="test_report_subject",
        state=SubscriptionState(
            modified_date=datetime.fromisoformat("2022-10-27T20:07:57+00:00")
        ),
    )
    test_data_2 = Subscription(
        email="test_user_email2@test.com",
        entity=SubscriptionEntity.GROUP,
        frequency=SubscriptionFrequency.MONTHLY,
        subject="test_report_subject2",
        state=SubscriptionState(
            modified_date=datetime.fromisoformat("2022-10-27T20:07:57+00:00")
        ),
    )
    await add(subscription=test_data_1)
    await add(subscription=test_data_2)

    loaders = get_new_context()

    assert await loaders.stakeholder_historic_subscription.load(
        (
            test_data_1.email,
            test_data_1.entity,
            test_data_1.subject,
        )
    ) == [test_data_1]

    assert await loaders.stakeholder_historic_subscription.load(
        (
            test_data_2.email,
            test_data_2.entity,
            test_data_2.subject,
        )
    ) == [test_data_2]

    await remove(
        email=test_data_1.email,
        entity=test_data_1.entity,
        subject=test_data_1.subject,
    )
    loaders.stakeholder_historic_subscription.clear_all()
    assert (
        await loaders.stakeholder_historic_subscription.load(
            (
                test_data_1.email,
                test_data_1.entity,
                test_data_1.subject,
            )
        )
        == []
    )

    assert await loaders.stakeholder_historic_subscription.load(
        (
            test_data_2.email,
            test_data_2.entity,
            test_data_2.subject,
        )
    ) == [test_data_2]
