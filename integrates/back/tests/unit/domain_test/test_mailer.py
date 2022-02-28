from context import (
    FI_MAIL_CUSTOMER_SUCCESS,
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
