# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import pytest
from sms.common import (
    send_sms_notification,
)
from unittest import (
    mock,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_send_sms_notification() -> None:
    test_phone_number = "12345678"
    test_message = "This is a test message"
    test_result = await send_sms_notification(  # type: ignore
        phone_number=test_phone_number,
        message_body=test_message,
    )
    assert test_result is None

    expected_sid = "SM87105da94bff44b999e4e6eb90d8eb6a"
    with mock.patch("sms.common.FI_ENVIRONMENT", "production"):
        with mock.patch("sms.common.client.messages.create") as mock_twilio:
            mock_twilio.return_value = expected_sid
            mock_result = await send_sms_notification(  # type: ignore
                phone_number=test_phone_number,
                message_body=test_message,
            )
    assert mock_twilio.called is True
    assert mock_result is None
