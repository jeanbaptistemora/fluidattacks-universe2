# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from custom_exceptions import (
    CouldNotVerifyStakeholder,
)
import pytest
from typing import (
    NamedTuple,
)
from unittest import (
    mock,
)
from verify.operations import (
    check_verification,
    get_country_code,
    start_verification,
    validate_mobile,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.skip(reason="Test should mock the Twilio response")
async def test_get_country_code() -> None:
    test_phone_number = "12345678"
    test_result = await get_country_code(test_phone_number)
    print(test_result)
    assert test_result == ""
    with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
        test_result = await get_country_code("+15108675310")
        assert test_result == "US"


async def test_check_verification() -> None:
    test_phone_number = "12345678"
    test_code = "US"
    test_result = await check_verification(  # type: ignore
        phone_number=test_phone_number, code=test_code
    )
    assert test_result is None
    with pytest.raises(CouldNotVerifyStakeholder):
        with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
            await check_verification(phone_number="", code=test_code)


@pytest.mark.skip(reason="Test should mock the Twilio response")
async def test_start_verification() -> None:
    test_phone_number = "12345678"
    test_result = await start_verification(
        phone_number=test_phone_number  # type: ignore
    )
    print(test_result)
    assert test_result is None
    with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
        await start_verification(phone_number="+15108675310")


async def test_validate_mobile() -> None:
    class MockedTwilioObject(NamedTuple):
        caller_name: str
        carrier: dict
        country_code: str
        national_format: str
        phone_number: str
        add_ons: str
        url: str

    test_phone_number = "12345678"
    test_result = await validate_mobile(test_phone_number)  # type: ignore
    assert test_result is None
    mocked_response = MockedTwilioObject(
        caller_name="null",
        carrier={
            "error_code": "null",
            "mobile_country_code": "310",
            "mobile_network_code": "456",
            "name": "verizon",
            "type": "mobile",
        },
        country_code="US",
        national_format="(510) 867-5310",
        phone_number="+15108675310",
        add_ons="null",
        url="https://lookups.twilio.com/v1/PhoneNumbers/+15108675310",
    )
    with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
        with mock.patch("verify.operations.client"):
            with mock.patch(
                "verify.operations.client.lookups.v1.phone_numbers"
            ) as mock_twilio:
                mock_twilio.return_value.fetch.return_value = mocked_response
                await validate_mobile("+15108675310")
    assert mock_twilio.called is True
