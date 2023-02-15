from back.test.functional.src.utils import (  # pylint: disable=import-error
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_result(
    *,
    card_number: str,
    card_expiration_month: str,
    card_expirations_year: str,
    card_cvc: str,
    make_default: bool,
    organization_id: str,
    user: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            addCreditCardPaymentMethod(
                organizationId: "{organization_id}",
                cardNumber: "{card_number}",
                cardExpirationMonth: "{card_expiration_month}",
                cardExpirationYear: "{card_expirations_year}",
                cardCvc: "{card_cvc}",
                makeDefault: {str(make_default).lower()},
            ) {{
                success
            }}
        }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
