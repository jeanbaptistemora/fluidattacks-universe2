# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import pytest
from sms.common import (
    send_sms_notification,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_send_sms_notification() -> None:
    test_phone_number = "12345678"
    test_message = "This is a test message"
    test_result = await send_sms_notification(
        phone_number=test_phone_number,
        message_body=test_message,
    )
    assert test_result is None
