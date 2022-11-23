from . import (
    get_result,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_stakeholder")
@pytest.mark.parametrize(
    ("email", "new_phone", "verification_code"),
    (
        (
            "admin@gmail.com",
            {"callingCountryCode": "1", "nationalNumber": "12345"},
            "12134",
        ),
    ),
)
async def test_verify_stakeholder(
    populate: bool,
    email: str,
    new_phone: Dict[str, str],
    verification_code: str,
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        new_phone=new_phone,
        verification_code=verification_code,
    )
    assert "errors" not in result
    assert result["data"]["verifyStakeholder"]["success"]
