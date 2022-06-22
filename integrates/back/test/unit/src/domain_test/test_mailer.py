# pylint: disable=too-many-arguments
from aioextensions import (
    collect,
)
from context import (
    FI_MAIL_CUSTOMER_SUCCESS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from group_access.domain import (
    get_group_users,
)
from groups.domain import (
    invite_to_group,
)
from mailer.common import (
    get_recipient_first_name,
)
from mailer.events import (
    send_mail_event_report,
)
import pytest


@pytest.mark.asyncio
async def test_get_recipient_first_name() -> None:
    assert (
        await get_recipient_first_name("nonexistinguser@fluidattacks.com")
        is None
    )
    assert (
        await get_recipient_first_name(FI_MAIL_CUSTOMER_SUCCESS.split(",")[0])
        is not None
    )
    assert (
        await get_recipient_first_name("integratesmanager@gmail.com")
        is not None
    )
    assert (
        await get_recipient_first_name(
            "nonexistinguser@fluidattacks.com", is_access_granted=True
        )
        is not None
    )

    loaders: Dataloaders = get_new_context()
    await invite_to_group(
        loaders=loaders,
        email="nonexistinguser@fluidattacks.com",
        responsibility="Tester",
        role="USER",
        group_name="oneshottest",
        modified_by="integratesmanager@gmail.com",
    )
    inactive_users = await get_group_users("oneshottest", active=False)
    active_users = await get_group_users("oneshottest", active=True)
    users = inactive_users + active_users
    recipients = await collect(
        tuple(get_recipient_first_name(email) for email in users)
    )

    assert len([recipient for recipient in recipients if recipient]) < len(
        users
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "group_name",
        "event_id",
        "event_type",
        "description",
        "reason",
        "other",
        "is_closed",
    ],
    [
        [
            "unittesting",
            "538745942",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "Test",
            None,
            None,
            False,
        ],
        [
            "unittesting",
            "538745942",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "Test",
            "PROBLEM_SOLVED",
            None,
            True,
        ],
        [
            "unittesting",
            "538745942",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "Test",
            "OTHER",
            "Test",
            True,
        ],
    ],
)
async def test_send_event_report(
    group_name: str,
    event_id: str,
    event_type: str,
    description: str,
    reason: str,
    other: str,
    is_closed: bool,
) -> None:
    await send_mail_event_report(
        loaders=get_new_context(),
        group_name=group_name,
        event_id=event_id,
        event_type=event_type,
        description=description,
        reason=reason,
        other=other,
        is_closed=is_closed,
        report_date=datetime(2022, 6, 16).date(),
    )
