# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from custom_exceptions import (
    CouldNotVerifyStakeholder,
)
import pytest
from unittest import (
    mock,
)
from verify.operations import (
    check_verification,
    get_contry_code,
    start_verification,
    validate_mobile,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.skip(reason="Test should mock the Twilio response")
async def test_get_contry_code() -> None:
    test_phone_number = "12345678"
    test_result = await get_contry_code(test_phone_number)
    print(test_result)
    assert test_result == ""
    with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
        test_result = await get_contry_code("+15108675310")
        assert test_result == "US"


async def test_check_verification() -> None:
    test_phone_number = "12345678"
    test_code = "US"
    test_result = await check_verification(
        phone_number=test_phone_number, code=test_code
    )
    assert test_result is None
    with pytest.raises(CouldNotVerifyStakeholder):
        with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
            await check_verification(phone_number="", code=test_code)


@pytest.mark.skip(reason="Test should mock the Twilio response")
async def test_start_verification() -> None:
    test_phone_number = "12345678"
    test_result = await start_verification(phone_number=test_phone_number)
    print(test_result)
    assert test_result is None
    with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
        await start_verification(phone_number="+15108675310")


@pytest.mark.skip(reason="Test should mock the Twilio response")
async def test_validate_mobile() -> None:
    test_phone_number = "12345678"
    test_result = await validate_mobile(test_phone_number)
    print(test_result)
    assert test_result is None
    with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
        await validate_mobile("+15108675310")
