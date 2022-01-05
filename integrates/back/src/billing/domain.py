from billing.types import (
    Customer,
    Portal,
    Price,
    Subscription,
)
from context import (
    BASE_URL,
    FI_STRIPE_API_KEY,
    FI_STRIPE_WEBHOOK_KEY,
)
from custom_exceptions import (
    BillingSubscriptionAlreadyActive,
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


async def _get_price(
    *,
    tier: str,
) -> Optional[Price]:
    """Return a tier price"""
    prices = stripe.Price.list(lookup_keys=[tier]).data
    if len(prices) > 0:
        return Price(
            id=prices[0].id,
            tier=prices[0].lookup_key,
        )
    return None


async def _get_group_subscription(
    *,
    group_name: str,
    org_billing_customer: str,
    limit: int = 1000,
    status: str = "all",
) -> Optional[Subscription]:
    """Return subscription for a group"""
    subs = stripe.Subscription.list(
        customer=org_billing_customer,
        limit=limit,
        status=status,
    ).data
    filtered = [sub for sub in subs if sub.metadata["group"] == group_name]
    if len(filtered) > 0:
        return Subscription(
            id=filtered[0].id,
            group=filtered[0].metadata["group"],
            org_billing_customer=filtered[0].customer,
            organization=filtered[0].metadata["organization"],
            tier=filtered[0].metadata["tier"],
        )
    return None


async def _group_has_active_subscription(
    *,
    group_name: str,
    org_billing_customer: str,
    tier: str,
) -> bool:
    """True if group has active subscription of tier type"""
    sub: Optional[Subscription] = await _get_group_subscription(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
        limit=1000,
    )
    if sub is not None and sub.tier == tier:
        return True
    return False


async def _set_group_tier(
    *,
    event_id: str,
    group_name: str,
    tier: str,
) -> bool:
    """Set a new tier for a group"""
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

    # Raise exception if group already has the same subscription active
    if await _group_has_active_subscription(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        tier=tier,
    ):
        raise BillingSubscriptionAlreadyActive()

    # Raise exception if Stripe price does not exist
    price: Optional[Price] = await _get_price(tier=tier)
    if price is None:
        raise InvalidBillingPrice()

    session_data = {
        "customer": org_billing_customer,
        "line_items": [
            {
                "price": price.id,
                "quantity": 1,
            },
        ],
        "metadata": {
            "group": group_name,
            "organization": org_name,
            "tier": tier,
        },
        "subscription_data": {
            "metadata": {
                "group": group_name,
                "organization": org_name,
                "tier": tier,
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
