from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_credit_card_payment_method")
@pytest.mark.parametrize(
    [
        "card_number",
        "card_expiration_month",
        "card_expirations_year",
        "card_cvc",
        "make_default",
    ],
    [
        ["378282246310005", "12", "27", "312", False],
        ["30569309025904", "11", "25", "055", False],
        ["5555555555554444", "10", "24", "123", False],
        ["4111111111111111", "04", "25", "123", True],
    ],
)
async def test_accept_legal(  # pylint: disable=too-many-arguments
    populate: bool,
    card_number: str,
    card_expiration_month: str,
    card_expirations_year: str,
    card_cvc: str,
    make_default: bool,
) -> None:
    assert populate
    user_email = "admin@fluidattacks.com"
    organization_id = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: dict[str, Any] = await get_result(
        card_number=card_number,
        card_expiration_month=card_expiration_month,
        card_expirations_year=card_expirations_year,
        card_cvc=card_cvc,
        make_default=make_default,
        organization_id=organization_id,
        user=user_email,
    )
    assert "errors" not in result
    assert result["data"]["addCreditCardPaymentMethod"]["success"]
