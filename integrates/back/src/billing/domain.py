from aioextensions import (
    collect,
)
from billing.types import (
    Customer,
    Invoice,
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
    BillingGroupWithoutSubscription,
    BillingSubscriptionAlreadyActive,
    InvalidBillingCustomer,
    InvalidBillingPrice,
)
from custom_types import (
    AddBillingSubscriptionPayload,
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
import time
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)

stripe.api_key = FI_STRIPE_API_KEY


async def _expire_checkout(
    *,
    checkout_id: str,
) -> bool:
    checkout = stripe.checkout.Session.retrieve(
        checkout_id,
    )
    if checkout.status == "open":
        return (
            stripe.checkout.Session.expire(
                checkout_id,
            ).status
            == "expired"
        )
    return True


async def _get_price(
    *,
    subscription: str,
    active: bool = True,
) -> Price:
    """Return a subscription price"""
    prices = stripe.Price.list(
        lookup_keys=[subscription],
        active=active,
    ).data
    if len(prices) > 0:
        return Price(
            id=prices[0].id,
            subscription=prices[0].lookup_key,
            metered=prices[0].recurring.aggregate_usage is not None,
        )
    raise InvalidBillingPrice()


async def _collect_subscription_prices(
    *,
    subscription: str,
) -> List[Price]:
    # Collect stripe prices
    prices: List[Price] = []
    if subscription == "squad":
        prices.extend(
            await collect(
                [
                    _get_price(
                        subscription=f"{subscription}_base",
                        active=True,
                    ),
                    _get_price(
                        subscription=f"{subscription}_recurring",
                        active=True,
                    ),
                ]
            )
        )
    else:
        prices.append(
            await _get_price(
                subscription=subscription,
                active=True,
            )
        )
    return prices


def _format_line_items(
    *,
    prices: List[Price],
) -> List[Dict[str, Any]]:
    line_items: List[Dict[str, Any]] = []
    for price in prices:
        if price.metered:
            line_items.append(
                {
                    "price": price.id,
                }
            )
        else:
            line_items.append(
                {
                    "price": price.id,
                    "quantity": 1,
                }
            )
    return line_items


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
    filtered = [sub for sub in subs if sub.metadata.group == group_name]
    if len(filtered) > 0:
        return Subscription(
            id=filtered[0].id,
            group=filtered[0].metadata.group,
            org_billing_customer=filtered[0].customer,
            organization=filtered[0].metadata.organization,
            type=filtered[0].metadata.subscription,
            items=[item["id"] for item in filtered[0]["items"]["data"]],
        )
    return None


async def _group_has_active_subscription(
    *,
    group_name: str,
    org_billing_customer: str,
    subscription: str,
) -> bool:
    """True if group has active subscription"""
    sub: Optional[Subscription] = await _get_group_subscription(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
        limit=1000,
    )
    if sub is not None and sub.type == subscription:
        return True
    return False


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


async def create_checkout(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
    previous_checkout_id: Optional[str],
) -> AddBillingSubscriptionPayload:
    """Create Stripe checkout session"""
    # Raise exception if group already has the same subscription active
    if await _group_has_active_subscription(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        subscription=subscription,
    ):
        raise BillingSubscriptionAlreadyActive()

    # Expire previous checkout if it is still open
    if previous_checkout_id is not None:
        await _expire_checkout(
            checkout_id=previous_checkout_id,
        )

    # Collect subscription prices
    prices: List[Price] = await _collect_subscription_prices(
        subscription=subscription
    )

    # Format checkout session data
    session_data = {
        "customer": org_billing_customer,
        "line_items": _format_line_items(prices=prices),
        "metadata": {
            "group": group_name,
            "organization": org_name,
            "subscription": subscription,
        },
        "subscription_data": {
            "metadata": {
                "group": group_name,
                "organization": org_name,
                "subscription": subscription,
            },
        },
        "mode": "subscription",
        "success_url": f"{BASE_URL}/orgs/{org_name}/billing",
        "cancel_url": f"{BASE_URL}/orgs/{org_name}/billing",
    }

    session = stripe.checkout.Session.create(**session_data)

    return AddBillingSubscriptionPayload(
        id=session.id,
        cancel_url=session.cancel_url,
        success=True,
        success_url=session.success_url,
        payment_url=session.url,
    )


async def create_portal(
    *,
    org_name: str,
    org_billing_customer: str,
) -> Portal:
    """Create Stripe portal session"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
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


async def update_subscription_preview(
    *,
    subscription: str,
    org_billing_customer: str,
    group_name: str,
) -> Invoice:
    """Preview a subscription update"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    sub: Optional[Subscription] = await _get_group_subscription(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
        limit=1000,
    )

    # Raise exception if group does not have an active subscription
    if sub is None:
        raise BillingGroupWithoutSubscription()

    # Raise exception if group already has the same subscription active
    if await _group_has_active_subscription(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        subscription=subscription,
    ):
        raise BillingSubscriptionAlreadyActive()

    # Collect subscription prices
    prices: List[Price] = await _collect_subscription_prices(
        subscription=subscription
    )
    proration_date: int = int(time.time())
    items: List[Dict[str, Any]] = []

    if subscription == "machine":
        items = [
            {
                "id": sub.items[0],
                "price": prices[0].id,
            },
            {
                "id": sub.items[1],
                "deleted": True,
            },
        ]
    else:
        items = [
            {
                "id": sub.items[0],
                "price": prices[0].id,
            },
        ]

    invoice = stripe.Invoice.upcoming(
        customer=org_billing_customer,
        subscription=sub.id,
        subscription_items=items,
        subscription_proration_date=proration_date,
    )

    return Invoice(
        account_name=invoice.account_name,
        amount_due=invoice.amount_due,
        amount_paid=invoice.amount_paid,
        amount_remaining=invoice.amount_remaining,
        data=invoice.lines.data,
    )


async def remove_subscription(
    *,
    group_name: str,
    org_billing_customer: str,
) -> bool:
    """Cancel a stripe subscription"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    sub: Optional[Subscription] = await _get_group_subscription(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
        limit=1000,
    )

    # Raise exception if group does not have an active subscription
    if sub is None:
        raise BillingGroupWithoutSubscription()

    return (
        stripe.Subscription.delete(
            sub.id,
        ).status
        == "canceled"
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
            if await groups_domain.update_group_tier(
                loaders=get_new_context(),
                reason=f"Update triggered by String with event {event.id}",
                requester_email="development@fluidattacks.com",
                group_name=event.data.object.metadata.group,
                tier=event.data.object.metadata.subscription,
            ):
                message = "Subscription creation was successful!"
        elif event.type == "customer.subscription.deleted":
            if await groups_domain.update_group_tier(
                loaders=get_new_context(),
                reason=f"Update triggered by String with event {event.id}",
                requester_email="development@fluidattacks.com",
                group_name=event.data.object.metadata.group,
                tier="free",
            ):
                message = "Subscription deletion was successful!"
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
