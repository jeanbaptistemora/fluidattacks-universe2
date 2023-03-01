from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
)
from custom_exceptions import (
    UnableToSendSms,
)
import pytest
from sms.common import (
    send_sms_notification,
)
from twilio.base.exceptions import (
    TwilioRestException,
)
from unittest.mock import (
    MagicMock,
    patch,
)

# Constants
MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["test_phone_number", "test_message", "expected_sid"],
    [
        [
            "12345678",
            "This is a test message",
            "SM87105da94bff44b999e4e6eb90d8eb6a",
        ]
    ],
)
@patch(MODULE_AT_TEST + "client.messages.create")
@patch(MODULE_AT_TEST + "FI_ENVIRONMENT", "production")
async def test_send_sms_notification(
    mock_twilio_client: MagicMock,
    test_phone_number: str,
    test_message: str,
    expected_sid: str,
) -> None:
    mock_twilio_client.return_value = expected_sid
    await send_sms_notification(
        phone_number=test_phone_number,
        message_body=test_message,
    )
    assert mock_twilio_client.called is True


@pytest.mark.parametrize(
    ["test_phone_number", "test_message"],
    [["12345678", "This is a test message"]],
)
@patch(MODULE_AT_TEST + "client.messages.create")
@patch(MODULE_AT_TEST + "FI_ENVIRONMENT", "production")
async def test_send_sms_notification_unable_to_send(
    mock_twilio_client: MagicMock,
    test_phone_number: str,
    test_message: str,
) -> None:
    status = 500
    uri = "/Accounts/ACXXXXXXXXXXXXXXXXX/Messages.json"
    mock_twilio_client.side_effect = TwilioRestException(status, uri)
    with pytest.raises(UnableToSendSms):
        await send_sms_notification(
            phone_number=test_phone_number,
            message_body=test_message,
        )
