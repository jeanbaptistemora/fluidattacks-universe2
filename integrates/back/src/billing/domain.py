from billing.types import (
    Customer,
    Portal,
)
from context import (
    BASE_URL,
    FI_STRIPE_API_KEY,
    FI_STRIPE_WEBHOOK_KEY,
)
from custom_exceptions import (
    InvalidBillingCustomer,
    InvalidBillingPrice,
    InvalidBillingTier,
)
from custom_types import (
    AddBillingCheckoutPayload,
)
from dataloaders import (
    get_new_context,
)
from groups import (
    domain as groups_domain,
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


async def _set_group_tier(
    *,
    event_id: str,
    group_name: str,
    tier: str,
) -> bool:
    data = {
        "loaders": get_new_context(),
        "group_name": group_name,
        "reason": f"Triggered by Stripe event {event_id}",
        "requester_email": "Integrates billing module",
        "comments": "",
        "subscription": "",
        "has_machine": False,
        "has_squad": False,
        "has_asm": True,
        "service": "",
        "tier": tier,
    }

    if tier == "machine":
        data["subscription"] = "continuous"
        data["has_machine"] = True
        data["has_squad"] = False
        data["service"] = "WHITE"
    elif tier == "squad":
        data["subscription"] = "continuous"
        data["has_machine"] = True
        data["has_squad"] = True
        data["service"] = "WHITE"
    elif tier == "oneshot":
        data["subscription"] = "oneshot"
        data["has_machine"] = False
        data["has_squad"] = False
        data["service"] = "BLACK"
    elif tier == "free":
        data["subscription"] = "continuous"
        data["has_machine"] = False
        data["has_squad"] = False
        data["service"] = "WHITE"
    else:
        raise InvalidBillingTier()

    return await groups_domain.update_group_attrs(**data)


async def create_customer(
    *,
    org_name: str,
    user_email: str,
) -> Customer:
    """Create Stripe customer"""
    customer = stripe.Customer.create(
        name=org_name,
        email=user_email,
    )

    return Customer(
        id=customer.id,
        name=customer.name,
        email=customer.email,
    )


async def checkout(
    *,
    tier: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
) -> AddBillingCheckoutPayload:
    """Create Stripe checkout session"""
    prices = stripe.Price.list(lookup_keys=[tier]).data
    if len(prices) > 0:
        price_id: str = prices[0].id
    else:
        raise InvalidBillingPrice()
    session_data = {
        "customer": org_billing_customer,
        "line_items": [
            {
                "price": price_id,
                "quantity": 1,
            },
        ],
        "metadata": {
            "organization": org_name,
            "group": group_name,
        },
        "subscription_data": {
            "metadata": {
                "organization": org_name,
                "group": group_name,
            },
        },
        "mode": "subscription",
        "success_url": f"{BASE_URL}/orgs/{org_name}/billing",
        "cancel_url": f"{BASE_URL}/orgs/{org_name}/billing",
    }

    session = stripe.checkout.Session.create(**session_data)

    return AddBillingCheckoutPayload(
        cancel_url=session.cancel_url,
        success=True,
        success_url=session.success_url,
        payment_url=session.url,
    )


async def portal(
    *,
    org_name: str,
    org_billing_customer: str,
) -> Portal:
    """Create Stripe portal session"""
    if org_billing_customer == "":
        raise InvalidBillingCustomer()

    session = stripe.billing_portal.Session.create(
        customer=org_billing_customer,
        return_url=f"{BASE_URL}/orgs/{org_name}/billing",
    )

    return Portal(
        organization=org_name,
        portal_url=session.url,
        return_url=session.return_url,
    )


async def webhook(request: Request) -> JSONResponse:
    """Parse Stripe webhook request and execute event"""

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

        if event.type == "customer.subscription.created":
            if await _set_group_tier(
                event_id=event.id,
                group_name=event.data.object.metadata.group,
                tier=event.data.object.plan.nickname,
            ):
                message = "Subscription was successful!"
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
