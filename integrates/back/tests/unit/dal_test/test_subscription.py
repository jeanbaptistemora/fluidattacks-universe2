from context import (
    FI_CHARTS_LOGO_PATH,
)
from decimal import (
    Decimal,
)
import os
import pytest
from subscriptions.dal import (
    get_subscriptions_to_entity_report,
    get_user_subscriptions,
    subscribe_user_to_entity_report,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_image_path() -> None:
    assert os.path.exists(FI_CHARTS_LOGO_PATH)


@pytest.mark.changes_db
async def test_update() -> None:
    await subscribe_user_to_entity_report(
        event_period=86400,
        report_entity="test_report_entity",
        report_subject="test_report_subject",
        user_email="test_user_email",
    )
    await subscribe_user_to_entity_report(
        event_period=3600.0,
        report_entity="test_report_entity",
        report_subject="test_report_subject2",
        user_email="test_user_email2",
    )
    await subscribe_user_to_entity_report(
        event_period=86400,
        report_entity="DIGEST",
        report_subject="ALL_GROUPS",
        user_email="test_user_email3",
    )

    assert await get_subscriptions_to_entity_report(audience="user",) == [
        {
            "period": Decimal("3600"),
            "pk": {
                "email": "integratesmanager@gmail.com",
                "meta": "user",
            },
            "pk_meta": "user",
            "sk": {
                "entity": "GROUP",
                "meta": "entity_report",
                "subject": "unittesting",
            },
            "sk_meta": "entity_report",
        },
        {
            "period": Decimal("86400"),
            "pk": {"email": "test_user_email", "meta": "user"},
            "pk_meta": "user",
            "sk": {
                "entity": "test_report_entity",
                "meta": "entity_report",
                "subject": "test_report_subject",
            },
            "sk_meta": "entity_report",
        },
        {
            "period": Decimal("3600"),
            "pk": {
                "email": "integratesuser@gmail.com",
                "meta": "user",
            },
            "pk_meta": "user",
            "sk": {
                "entity": "DIGEST",
                "meta": "entity_report",
                "subject": "ALL_GROUPS",
            },
            "sk_meta": "entity_report",
        },
        {
            "period": Decimal("86400"),
            "pk": {"email": "test_user_email3", "meta": "user"},
            "pk_meta": "user",
            "sk": {
                "entity": "DIGEST",
                "meta": "entity_report",
                "subject": "ALL_GROUPS",
            },
            "sk_meta": "entity_report",
        },
        {
            "period": Decimal("3600"),
            "pk": {"email": "test_user_email2", "meta": "user"},
            "pk_meta": "user",
            "sk": {
                "entity": "test_report_entity",
                "meta": "entity_report",
                "subject": "test_report_subject2",
            },
            "sk_meta": "entity_report",
        },
        {
            "period": Decimal("86400"),
            "pk": {
                "email": "integratesmanager@fluidattacks.com",
                "meta": "user",
            },
            "pk_meta": "user",
            "sk": {
                "entity": "GROUP",
                "meta": "entity_report",
                "subject": "unittesting",
            },
            "sk_meta": "entity_report",
        },
    ]
    assert await get_user_subscriptions(user_email="test_user_email",) == [
        {
            "period": Decimal("86400"),
            "pk": {"email": "test_user_email", "meta": "user"},
            "pk_meta": "user",
            "sk": {
                "entity": "test_report_entity",
                "meta": "entity_report",
                "subject": "test_report_subject",
            },
            "sk_meta": "entity_report",
        }
    ]
    assert await get_user_subscriptions(user_email="test_user_email2",) == [
        {
            "period": Decimal("3600"),
            "pk": {"email": "test_user_email2", "meta": "user"},
            "pk_meta": "user",
            "sk": {
                "entity": "test_report_entity",
                "meta": "entity_report",
                "subject": "test_report_subject2",
            },
            "sk_meta": "entity_report",
        }
    ]
    assert await get_user_subscriptions(
        user_email="integratesmanager@gmail.com",
    ) == [
        {
            "period": Decimal("3600"),
            "pk": {
                "email": "integratesmanager@gmail.com",
                "meta": "user",
            },
            "pk_meta": "user",
            "sk": {
                "entity": "GROUP",
                "meta": "entity_report",
                "subject": "unittesting",
            },
            "sk_meta": "entity_report",
        }
    ]
    assert await get_user_subscriptions(
        user_email="integratesuser@gmail.com",
    ) == [
        {
            "period": Decimal("3600"),
            "pk": {
                "email": "integratesuser@gmail.com",
                "meta": "user",
            },
            "pk_meta": "user",
            "sk": {
                "entity": "DIGEST",
                "meta": "entity_report",
                "subject": "ALL_GROUPS",
            },
            "sk_meta": "entity_report",
        }
    ]
    assert await get_user_subscriptions(
        user_email="integratesmanager@fluidattacks.com",
    ) == [
        {
            "period": Decimal("86400"),
            "pk": {
                "email": "integratesmanager@fluidattacks.com",
                "meta": "user",
            },
            "pk_meta": "user",
            "sk": {
                "entity": "GROUP",
                "meta": "entity_report",
                "subject": "unittesting",
            },
            "sk_meta": "entity_report",
        }
    ]
