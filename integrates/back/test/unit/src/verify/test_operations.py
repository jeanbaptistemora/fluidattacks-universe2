import pytest
from verify.operations import (
    get_contry_code,
    start_verification,
    validate_mobile,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_contry_code() -> None:
    test_phone_number = "12345678"
    test_result = await get_contry_code(test_phone_number)
    print(test_result)
    assert test_result == ""


async def test_start_verification() -> None:
    test_phone_number = "12345678"
    test_result = await start_verification(phone_number=test_phone_number)
    print(test_result)
    assert test_result is None


async def test_validate_mobile() -> None:
    test_phone_number = "12345678"
    test_result = await validate_mobile(test_phone_number)
    print(test_result)
    assert test_result is None
