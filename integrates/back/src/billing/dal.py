from aioextensions import (
    collect,
)
from bill import (
    domain as bill_domain,
)
from billing.types import (
    Customer,
    PaymentMethod,
    Portal,
    Price,
    Subscription,
    SubscriptionItem,
)
from context import (
    BASE_URL,
    FI_STRIPE_API_KEY,
)
from custom_exceptions import (
    InvalidBillingCustomer,
    InvalidBillingPrice,
)
from datetime import (
    datetime,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
import stripe
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

stripe.api_key = FI_STRIPE_API_KEY


async def _format_create_subscription_data(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
) -> Dict[str, Any]:
    """Format create subscription session data according to stripe API"""
    prices: List[Price] = await get_subscription_prices(
        subscription=subscription,
    )
    items: List[Dict[str, Any]] = []
    for price in prices:
        if price.subscription == "machine":
            items.append(
                {
                    "price": price.id,
                    "quantity": 1,
                }
            )
        else:
            items.append(
                {
                    "price": price.id,
                }
            )
    billing_cycle_anchor: int = int(
        datetime_utils.get_first_day_next_month_timestamp()
    )

    return {
        "customer": org_billing_customer,
        "items": items,
        "metadata": {
            "group": group_name,
            "organization": org_name,
            "subscription": subscription,
        },
        "billing_cycle_anchor": billing_cycle_anchor,
    }


async def attach_payment_method(
    *,
    payment_method_id: str,
    org_billing_customer: str,
) -> bool:
    """Attach a payment method to a Stripe customer"""
    data = stripe.PaymentMethod.attach(
        payment_method_id,
        customer=org_billing_customer,
    )
    return isinstance(data.created, int)


async def create_customer(
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


async def create_payment_method(
    *,
    card_number: str,
    card_expiration_month: str,
    card_expiration_year: str,
    card_cvc: str,
) -> PaymentMethod:
    """Create a Stripe payment method"""
    data = stripe.PaymentMethod.create(
        type="card",
        card={
            "number": card_number,
            "exp_month": int(card_expiration_month),
            "exp_year": int(card_expiration_year),
            "cvc": card_cvc,
        },
    )
    return PaymentMethod(
        id=data.id,
        last_four_digits=data.card.last4,
        expiration_month=str(data.card.exp_month),
        expiration_year=str(data.card.exp_year),
        brand=data.card.brand,
    )


async def create_subscription(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
) -> bool:
    """Create stripe subscription"""
    data: Dict[str, Any] = await _format_create_subscription_data(
        subscription=subscription,
        org_billing_customer=org_billing_customer,
        org_name=org_name,
        group_name=group_name,
    )
    sub = stripe.Subscription.create(**data)
    return isinstance(sub.created, int)


async def create_portal(
    *,
    org_billing_customer: str,
    org_name: str,
) -> Portal:
    """Create Stripe portal session"""
    data = stripe.billing_portal.Session.create(
        customer=org_billing_customer,
        return_url=f"{BASE_URL}/orgs/{org_name}/billing",
    )
    return Portal(
        organization=org_name,
        portal_url=data.url,
        return_url=data.return_url,
    )


async def get_price(
    *,
    subscription: str,
    active: bool = True,
) -> Price:
    """Return a subscription price"""
    data = stripe.Price.list(
        lookup_keys=[subscription],
        active=active,
    ).data
    if len(data) > 0:
        return Price(
            id=data[0].id,
            subscription=data[0].lookup_key,
        )
    raise InvalidBillingPrice()


async def get_subscription(
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


async def get_customer(
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


async def get_customer_payment_methods(
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


async def get_subscription_prices(
    *,
    subscription: str,
) -> List[Price]:
    # Collect stripe prices
    prices = [
        get_price(
            subscription=subscription,
            active=True,
        )
    ]

    # Add machine base price if subscription is squad
    if subscription == "squad":
        prices.append(
            get_price(
                subscription="machine",
                active=True,
            )
        )
    return await collect(prices)


async def set_default_payment_method(
    *,
    payment_method_id: str,
    org_billing_customer: str,
) -> bool:
    """Make a payment method default for a customer"""
    data = stripe.Customer.modify(
        org_billing_customer,
        invoice_settings={"default_payment_method": payment_method_id},
    )
    return data.invoice_settings.default_payment_method == payment_method_id


async def report_subscription_usage(
    *,
    subscription: Subscription,
) -> None:
    """Report group squad usage to Stripe"""
    timestamp: int = int(datetime_utils.get_utc_timestamp())
    date: datetime = datetime_utils.get_utc_now()
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
