# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from context import (
    FI_INTEGRATES_REPORTS_LOGO_PATH,
)
from dataloaders import (
    get_new_context,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from db_model.subscriptions.types import (
    Subscription,
)
from newutils.subscriptions import (
    translate_entity,
)
import os
import pytest
from subscriptions.dal import (
    add,
    get_all_subscriptions,
)

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
    )
    test_data_2 = Subscription(
        email="test_user_email2@test.com",
        entity=SubscriptionEntity.GROUP,
        frequency=SubscriptionFrequency.MONTHLY,
        subject="test_report_subject2",
    )
    await add(subscription=test_data_1)
    await add(subscription=test_data_2)

    assert await get_all_subscriptions(
        frequency=SubscriptionFrequency.HOURLY
    ) == (
        Subscription(
            email="integratesmanager@gmail.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.HOURLY,
            subject="unittesting",
        ),
    )
    assert await get_all_subscriptions(
        frequency=SubscriptionFrequency.DAILY
    ) == (
        Subscription(
            email="integratesmanager@fluidattacks.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.DAILY,
            subject="unittesting",
        ),
    )
    assert await get_all_subscriptions(
        frequency=SubscriptionFrequency.WEEKLY
    ) == (
        Subscription(
            email="test_user_email@test.com",
            entity=SubscriptionEntity.ORGANIZATION,
            frequency=SubscriptionFrequency.WEEKLY,
            subject="test_report_subject",
        ),
    )
    assert await get_all_subscriptions(
        frequency=SubscriptionFrequency.MONTHLY
    ) == (
        Subscription(
            email="test_user_email2@test.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.MONTHLY,
            subject="test_report_subject2",
        ),
        Subscription(
            email="integratesmanager@fluidattacks.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.MONTHLY,
            subject="oneshottest",
        ),
    )

    loaders = get_new_context()

    assert await loaders.stakeholder_subscriptions.load(test_data_1.email) == (
        Subscription(
            email="test_user_email@test.com",
            entity=SubscriptionEntity.ORGANIZATION,
            frequency=SubscriptionFrequency.WEEKLY,
            subject="test_report_subject",
        ),
    )
    assert await loaders.stakeholder_subscriptions.load(test_data_2.email) == (
        Subscription(
            email="test_user_email2@test.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.MONTHLY,
            subject="test_report_subject2",
        ),
    )
    assert await loaders.stakeholder_subscriptions.load(
        "integratesmanager@gmail.com",
    ) == (
        Subscription(
            email="integratesmanager@gmail.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.HOURLY,
            subject="unittesting",
        ),
    )
    assert await loaders.stakeholder_subscriptions.load(
        "integratesmanager@fluidattacks.com",
    ) == (
        Subscription(
            email="integratesmanager@fluidattacks.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.MONTHLY,
            subject="oneshottest",
        ),
        Subscription(
            email="integratesmanager@fluidattacks.com",
            entity=SubscriptionEntity.GROUP,
            frequency=SubscriptionFrequency.DAILY,
            subject="unittesting",
        ),
    )
