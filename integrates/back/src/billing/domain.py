from aioextensions import (
    collect,
)
from bill import (
    domain as bill_domain,
)
from billing.types import (
    AddBillingSubscriptionPayload,
    Customer,
    PaymentMethod,
    Portal,
    Price,
    Subscription,
    SubscriptionItem,
    UpdateBillingSubscriptionPayload,
)
from context import (
    BASE_URL,
    FI_STRIPE_API_KEY,
    FI_STRIPE_WEBHOOK_KEY,
)
from custom_exceptions import (
    BillingGroupActiveSubscription,
    BillingGroupWithoutSubscription,
    BillingSubscriptionSameActive,
    InvalidBillingCustomer,
    InvalidBillingPrice,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
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
        )
    raise InvalidBillingPrice()


async def _collect_subscription_prices(
    *,
    subscription: str,
) -> List[Price]:
    # Collect stripe prices
    prices = [
        _get_price(
            subscription=subscription,
            active=True,
        )
    ]

    # Add machine base price if subscription is squad
    if subscription == "squad":
        prices.append(
            _get_price(
                subscription="machine",
                active=True,
            )
        )
    return await collect(prices)


async def _format_create_subscription_data(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
) -> Dict[str, Any]:
    """Format create subscription session data according to stripe API"""
    prices: List[Price] = await _collect_subscription_prices(
        subscription=subscription,
    )
    line_items: List[Dict[str, Any]] = []
    for price in prices:
        if price.subscription == "machine":
            line_items.append(
                {
                    "price": price.id,
                    "quantity": 1,
                }
            )
        else:
            line_items.append(
                {
                    "price": price.id,
                }
            )

    return {
        "customer": org_billing_customer,
        "line_items": line_items,
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


async def _format_update_subscription_data(
    *,
    org_billing_customer: str,
    subscription_id: str,
    subscription: str,
    current_items: List[SubscriptionItem],
) -> Dict[str, Any]:
    """Format update subscription session data according to stripe API"""
    prices: List[Price] = await _collect_subscription_prices(
        subscription=subscription,
    )
    proration_date: int = int(time.time())
    items: List[Dict[str, Any]] = []

    if subscription == "machine":
        items = [
            {
                "id": current_items[0].id,
                "price": prices[0].id,
            },
            {
                "id": current_items[1].id,
                "deleted": True,
                "clear_usage": True,
            },
        ]
    else:
        items = [
            {
                "id": current_items[0].id,
                "price": prices[0].id,
            },
            {
                "price": prices[1].id,
            },
        ]

    return {
        "customer": org_billing_customer,
        "subscription": subscription_id,
        "subscription_items": items,
        "subscription_proration_date": proration_date,
    }


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
        sub_items: List[SubscriptionItem] = [
            SubscriptionItem(
                id=item["id"],
                type=item["price"]["lookup_key"],
            )
            for item in filtered[0]["items"]["data"]
        ]
        return Subscription(
            id=filtered[0].id,
            group=filtered[0].metadata.group,
            org_billing_customer=filtered[0].customer,
            organization=filtered[0].metadata.organization,
            type=filtered[0].metadata.subscription,
            items=sub_items,
        )
    return None


async def _group_has_active_subscription(
    *,
    group_name: str,
    org_billing_customer: str,
) -> bool:
    """True if group has active subscription"""
    sub: Optional[Subscription] = await _get_group_subscription(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
        limit=1000,
    )
    return sub is not None


async def _create_customer(
    *,
    org_id: str,
    org_name: str,
    user_email: str,
) -> Customer:
    """Create Stripe customer"""
    # Create customer in stripe
    stripe_customer = stripe.Customer.create(
        name=org_name,
        email=user_email,
    )
    customer: Customer = Customer(
        id=stripe_customer.id,
        name=stripe_customer.name,
        email=stripe_customer.email,
        default_payment_method=None,
    )

    # Assign customer to org
    await orgs_domain.update_billing_customer(
        org_id=org_id,
        org_name=org_name,
        org_billing_customer=customer.id,
    )

    return customer


async def _get_customer(
    *,
    org_billing_customer: str,
) -> Customer:
    """Retrieve Stripe customer"""
    stripe_customer = stripe.Customer.retrieve(
        org_billing_customer,
    )
    default_payment_method: Optional[
        str
    ] = stripe_customer.invoice_settings.default_payment_method
    return Customer(
        id=stripe_customer.id,
        name=stripe_customer.name,
        email=stripe_customer.email,
        default_payment_method=default_payment_method,
    )


async def _report_subscription_usage(
    *,
    subscription: Subscription,
) -> None:
    """Report group squad usage to Stripe"""
    timestamp: int = int(time.time())
    date: datetime = datetime_utils.get_now()
    authors: int = len(
        await bill_domain.get_authors_data(
            date=date,
            group=subscription.group,
        )
    )
    sub_item_id: str = [
        item.id for item in subscription.items if item.type == "squad"
    ][0]

    stripe.SubscriptionItem.create_usage_record(
        sub_item_id,
        quantity=authors,
        timestamp=timestamp,
        action="set",
    )


async def customer_payment_methods(
    *, org_billing_customer: str, limit: int = 100
) -> List[PaymentMethod]:
    """Return list of customer's payment methods"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    payment_methods = stripe.Customer.list_payment_methods(
        org_billing_customer,
        type="card",
        limit=limit,
    ).data
    return [
        PaymentMethod(
            id=payment_method.id,
            last_four_digits=payment_method.card.last4,
            expiration_month=str(payment_method.card.exp_month),
            expiration_year=str(payment_method.card.exp_year),
            brand=payment_method.card.brand,
        )
        for payment_method in payment_methods
    ]


async def create_payment_method(
    *,
    org_billing_customer: Optional[str],
    org_id: str,
    org_name: str,
    user_email: str,
    card_number: str,
    card_expiration_month: str,
    card_expiration_year: str,
    card_cvc: str,
    make_default: bool,
) -> bool:
    """Create a payment method and associate it to the customer"""
    # Create customer if it does not exist
    customer: Optional[Customer] = None
    if org_billing_customer is None:
        customer = await _create_customer(
            org_id=org_id,
            org_name=org_name,
            user_email=user_email,
        )
    else:
        customer = await _get_customer(
            org_billing_customer=org_billing_customer,
        )

    # Create payment method
    payment_method = stripe.PaymentMethod.create(
        type="card",
        card={
            "number": card_number,
            "exp_month": int(card_expiration_month),
            "exp_year": int(card_expiration_year),
            "cvc": card_cvc,
        },
    )

    # Attach payment method to customer
    attachment = stripe.PaymentMethod.attach(
        payment_method.id,
        customer=customer.id,
    )

    # If payment method is the first one registered or selected as default,
    # then make it default
    if not customer.default_payment_method or make_default:
        stripe.Customer.modify(
            customer.id,
            invoice_settings={"default_payment_method": payment_method.id},
        )

    return isinstance(attachment.created, int)


async def create_subscription(
    *,
    subscription: str,
    org_billing_customer: Optional[str],
    org_id: str,
    org_name: str,
    group_name: str,
    previous_checkout_id: Optional[str],
    user_email: str,
) -> AddBillingSubscriptionPayload:
    """Create Stripe checkout session"""
    # Create customer if it does not exist
    if org_billing_customer is None:
        customer: Customer = await _create_customer(
            org_id=org_id,
            org_name=org_name,
            user_email=user_email,
        )
        org_billing_customer = customer.id

    # Raise exception if group already has an active subscription
    if await _group_has_active_subscription(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
    ):
        raise BillingGroupActiveSubscription()

    # Expire previous checkout if it is still open
    if previous_checkout_id is not None:
        await _expire_checkout(
            checkout_id=previous_checkout_id,
        )

    # Format subscription creation data
    data: Dict[str, Any] = await _format_create_subscription_data(
        subscription=subscription,
        org_billing_customer=org_billing_customer,
        org_name=org_name,
        group_name=group_name,
    )

    session = stripe.checkout.Session.create(**data)
    checkout = AddBillingSubscriptionPayload(
        id=session.id,
        cancel_url=session.cancel_url,
        success=True,
        success_url=session.success_url,
        payment_url=session.url,
    )

    # Update group with new billing checkout id
    await groups_domain.update_billing_checkout_id(
        group_name,
        checkout.id,
    )

    return checkout


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


async def update_subscription(
    *,
    subscription: str,
    org_billing_customer: str,
    group_name: str,
    preview: bool,
) -> UpdateBillingSubscriptionPayload:
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
    if sub.type == subscription:
        raise BillingSubscriptionSameActive()

    # Report latest usage if subscription is squad
    if sub.type == "squad":
        await _report_subscription_usage(
            subscription=sub,
        )

    # Format subscription update data
    data = await _format_update_subscription_data(
        org_billing_customer=org_billing_customer,
        subscription_id=sub.id,
        subscription=subscription,
        current_items=sub.items,
    )

    invoice = stripe.Invoice.upcoming(**data)

    # Update subscription if not a preview
    if not preview:
        stripe.Subscription.modify(
            sub.id,
            cancel_at_period_end=False,
            proration_behavior="create_prorations",
            items=data["subscription_items"],
            metadata={"subscription": subscription},
        )

    return UpdateBillingSubscriptionPayload(
        amount_due=invoice.amount_due,
        amount_paid=invoice.amount_paid,
        amount_remaining=invoice.amount_remaining,
        success=True,
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

    # Report usage if subscription is squad
    invoice_now: bool = False
    if sub.type == "squad":
        await _report_subscription_usage(
            subscription=sub,
        )
        invoice_now = True

    return (
        stripe.Subscription.delete(
            sub.id,
            invoice_now=invoice_now,
            prorate=True,
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

        if event.type in (
            "customer.subscription.created",
            "customer.subscription.updated",
        ):
            if await groups_domain.update_group_tier(
                loaders=get_new_context(),
                reason=f"Update triggered by String with event {event.id}",
                requester_email="development@fluidattacks.com",
                group_name=event.data.object.metadata.group,
                tier=event.data.object.metadata.subscription,
            ):
                message = "Subscription successful!"
        elif event.type == "customer.subscription.deleted":
            if await groups_domain.update_group_tier(
                loaders=get_new_context(),
                reason=f"Update triggered by String with event {event.id}",
                requester_email="development@fluidattacks.com",
                group_name=event.data.object.metadata.group,
                tier="free",
            ):
                message = "Subscription deletion successful!"
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
