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
    await send_sms_notification(
        phone_number=test_phone_number,
        message_body=test_message,
    )

    expected_sid = "SM87105da94bff44b999e4e6eb90d8eb6a"
    with mock.patch("sms.common.FI_ENVIRONMENT", "production"):
        with mock.patch("sms.common.client.messages.create") as mock_twilio:
            mock_twilio.return_value = expected_sid
            await send_sms_notification(
                phone_number=test_phone_number,
                message_body=test_message,
            )
    assert mock_twilio.called is True
