from aioextensions import (
    collect,
)
from context import (
    FI_MAIL_CUSTOMER_SUCCESS,
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

    await invite_to_group(
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
