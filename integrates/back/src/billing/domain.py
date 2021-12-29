from billing.types import (
    Checkout,
    Portal,
)
from context import (
    BASE_URL,
    FI_STRIPE_API_KEY,
    FI_STRIPE_WEBHOOK_KEY,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
)
import stripe
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)

stripe.api_key = FI_STRIPE_API_KEY


async def checkout(
    *,
    tier: str,
    org_name: str,
    group_name: str,
) -> Checkout:

    price_id: str = stripe.Price.list(lookup_keys=[tier]).data[0].id
    session = stripe.checkout.Session.create(
        client_reference_id=group_name,
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            },
        ],
        mode="subscription",
        success_url=f"{BASE_URL}/orgs/{org_name}/billing",
        cancel_url=f"{BASE_URL}/orgs/{org_name}/billing",
    )

    return Checkout(
        cancel_url=session.cancel_url,
        success_url=session.success_url,
        payment_url=session.url,
    )


async def portal(
    *,
    org_name: str,
    group_name: str,
) -> Portal:
    session = stripe.billing_portal.Session.create(
        customer=group_name,
        return_url=f"{BASE_URL}/orgs/{org_name}/billing",
    )

    return Portal(
        group=group_name,
        portal_url=session.url,
        return_url=session.return_url,
    )


async def webhook(request: Request) -> JSONResponse:
    """Parse webhook request and execute event"""

    body: Optional[bytes] = await request.body()
    signature: Optional[str] = request.headers.get("stripe-signature")
    message: str = ""
    status: str = "success"

    try:
        event = stripe.Webhook.construct_event(
            body,
            signature,
            FI_STRIPE_WEBHOOK_KEY,
        )

        if event.type == "payment_intent.succeeded":
            message = "PaymentIntent was successful!"
        else:
            message = f"Unhandled event type: {event.type}"
            status = "failed"
            LOGGER.warning(message, extra=dict(extra=locals()))
    except ValueError as ex:
        message = "Invalid payload"
        status = "failed"
        LOGGER.exception(ex, extra=dict(extra=locals()))
    except stripe.error.SignatureVerificationError as ex:
        message = "Invalid signature"
        status = "failed"
        LOGGER.exception(ex, extra=dict(extra=locals()))

    return JSONResponse(
        {
            "status": status,
            "message": message,
        }
    )
