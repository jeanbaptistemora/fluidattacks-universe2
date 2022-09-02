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
from group_access.domain import (
    get_group_stakeholders_emails,
)
from groups.domain import (
    invite_to_group,
)
from mailer.common import (
    get_recipient_first_name,
    get_recipients,
)
import pytest


@pytest.mark.asyncio
async def test_get_recipient_first_name() -> None:
    loaders: Dataloaders = get_new_context()
    assert (
        await get_recipient_first_name(
            loaders, "nonexistinguser@fluidattacks.com"
        )
        is None
    )
    assert (
        await get_recipient_first_name(
            loaders, FI_MAIL_CUSTOMER_SUCCESS.split(",")[0]
        )
        is not None
    )
    assert (
        await get_recipient_first_name(loaders, "integratesmanager@gmail.com")
        is not None
    )
    assert (
        await get_recipient_first_name(
            loaders, "nonexistinguser@fluidattacks.com", is_access_granted=True
        )
        is not None
    )

    await invite_to_group(
        loaders=loaders,
        email="nonexistinguser@fluidattacks.com",
        responsibility="Tester",
        role="USER",
        group_name="oneshottest",
        modified_by="integratesmanager@gmail.com",
    )
    inactive_users = await get_group_stakeholders_emails(
        get_new_context(), "oneshottest", active=False
    )
    active_users = await get_group_stakeholders_emails(
        get_new_context(), "oneshottest", active=True
    )
    users = inactive_users + active_users
    recipients = await collect(
        tuple(get_recipient_first_name(loaders, email) for email in users)
    )

    assert len([recipient for recipient in recipients if recipient]) < len(
        users
    )


@pytest.mark.asyncio
async def test_get_recipients() -> None:
    loaders: Dataloaders = get_new_context()
    assert await get_recipients(
        loaders=loaders,
        email_to="integratesmanager@gmail.com",
        email_cc=["nonexisting@nonexisting.com"],
        first_name="Integrates",
        is_access_granted=False,
    ) == [
        {
            "email": "integratesmanager@gmail.com",
            "name": "Integrates",
            "type": "to",
        }
    ]
    assert await get_recipients(
        loaders=loaders,
        email_to="integratesmanager@gmail.com",
        email_cc=["unittest@fluidattacks.com"],
        first_name="Integrates",
        is_access_granted=False,
    ) == [
        {
            "email": "integratesmanager@gmail.com",
            "name": "Integrates",
            "type": "to",
        },
        {"email": "unittest@fluidattacks.com", "name": "Miguel", "type": "cc"},
    ]
    assert await get_recipients(
        loaders=loaders,
        email_to="integratesmanager@gmail.com",
        email_cc=None,
        first_name="Integrates",
        is_access_granted=False,
    ) == [
        {
            "email": "integratesmanager@gmail.com",
            "name": "Integrates",
            "type": "to",
        }
    ]
