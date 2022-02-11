from billing.types import (
    Customer,
    PaymentMethod,
    Price,
    Subscription,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    BASE_URL,
    FI_STRIPE_API_KEY,
    FI_STRIPE_WEBHOOK_KEY,
    SERVICES_AWS_S3_DATA_BUCKET as SERVICES_DATA_BUCKET,
)
import csv
from custom_exceptions import (
    CouldNotDowngradeSubscription,
)
from datetime import (
    datetime,
)
import io
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
import os
from s3.operations import (
    aio_client,
)
from settings import (
    LOGGING,
)
from starlette.requests import (
    Request,
)
import stripe
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

stripe.api_key = FI_STRIPE_API_KEY
logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_billing_buffer(*, date: datetime, group: str) -> io.BytesIO:
    year: str = date.strftime("%Y")
    month: str = date.strftime("%m")
    # The day is also available after 2019-09 in case it's needed

    buffer = io.BytesIO()

    key: str = os.path.join("bills", year, month, f"{group}.csv")

    try:
        async with aio_client() as client:
            await client.download_fileobj(SERVICES_DATA_BUCKET, key, buffer)
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    else:
        buffer.seek(0)

    return buffer


async def _pay_squad_authors_to_date(
    *,
    prices: Dict[str, Price],
    subscription: Subscription,
) -> bool:
    """Pay squad authors to date"""
    authors: int = await _get_subscription_usage(subscription=subscription)
    customer: Customer = await get_customer(
        org_billing_customer=subscription.org_billing_customer,
    )

    return (
        stripe.PaymentIntent.create(
            customer=subscription.org_billing_customer,
            amount=prices["squad"].amount * authors,
            currency=prices["squad"].currency,
            payment_method=customer.default_payment_method,
            confirm=True,
        ).status
        == "succeeded"
    )


async def _get_subscription_usage(
    *,
    subscription: Subscription,
) -> int:
    """Get group squad usage"""
    date: datetime = datetime_utils.get_utc_now()
    return len(
        await get_authors_data(
            date=date,
            group=subscription.group,
        )
    )


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


async def create_webhook_event(
    *,
    request: Request,
) -> Any:
    return stripe.Webhook.construct_event(
        await request.body(),
        request.headers.get("stripe-signature"),
        FI_STRIPE_WEBHOOK_KEY,
    )


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
    default: bool,
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
        default=default,
    )


async def create_subscription(
    *,
    customer: str,
    items: List[Dict[str, Any]],
    metadata: Dict[str, str],
    billing_cycle_anchor: int,
) -> bool:
    """Create stripe subscription"""
    sub = stripe.Subscription.create(
        customer=customer,
        items=items,
        metadata=metadata,
        billing_cycle_anchor=billing_cycle_anchor,
    )
    return sub.status == "active"


async def create_portal(
    *,
    org_billing_customer: str,
    org_name: str,
) -> str:
    """Create Stripe portal session"""
    return stripe.billing_portal.Session.create(
        customer=org_billing_customer,
        return_url=f"{BASE_URL}/orgs/{org_name}/billing",
    ).url


async def get_prices() -> Dict[str, Price]:
    """Get model prices"""
    data = stripe.Price.list(
        lookup_keys=[
            "machine",
            "squad",
        ],
        active=True,
    ).data

    return {
        price.lookup_key: Price(
            id=price.id,
            currency=price.currency,
            amount=price.unit_amount,
            type=price.type,
        )
        for price in data
    }


async def get_customer_subscriptions(
    *,
    org_billing_customer: str,
    limit: int = 1000,
    status: str = "active",
) -> Dict[str, Subscription]:
    subs = stripe.Subscription.list(
        customer=org_billing_customer,
        limit=limit,
        status=status,
    ).data
    return {
        f"{sub.metadata.group}__{sub.metadata.subscription}": Subscription(
            id=sub.id,
            group=sub.metadata.group,
            org_billing_customer=sub.customer,
            organization=sub.metadata.organization,
            status=sub.status,
            type=sub.metadata.subscription,
            items={
                item["metadata"]["name"]: item["id"]
                for item in sub["items"]["data"]
            },
        )
        for sub in subs
    }


async def get_group_subscriptions(
    *,
    group_name: str,
    org_billing_customer: str,
    status: str = "",
) -> List[Subscription]:
    """Return subscription history for a group"""
    data: Dict[str, Any] = {
        "customer": org_billing_customer,
        "limit": 1000,
    }
    if status != "":
        data["status"] = status

    subs = stripe.Subscription.list(**data).data
    filtered = [sub for sub in subs if sub.metadata.group == group_name]
    return [
        Subscription(
            id=sub.id,
            group=sub.metadata.group,
            org_billing_customer=sub.customer,
            organization=sub.metadata.organization,
            status=sub.status,
            type=sub.metadata.subscription,
            items={
                item["metadata"]["name"]: item["id"]
                for item in sub["items"]["data"]
            },
        )
        for sub in filtered
    ]


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
) -> List[Dict[str, Any]]:
    """Return list of customer's payment methods"""
    return stripe.Customer.list_payment_methods(
        org_billing_customer,
        type="card",
        limit=limit,
    ).data


async def update_default_payment_method(
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


async def remove_payment_method(
    *,
    payment_method_id: str,
) -> bool:
    return (
        stripe.PaymentMethod.detach(
            payment_method_id,
        ).customer
        is None
    )


async def remove_subscription(
    *,
    subscription_id: str,
    invoice_now: bool,
    prorate: bool,
) -> bool:
    """Remove a stripe subscription"""
    result: str = stripe.Subscription.delete(
        subscription_id,
        invoice_now=invoice_now,
        prorate=prorate,
    ).status

    return result in ("canceled", "incomplete_expired")


async def report_subscription_usage(
    *,
    subscription: Subscription,
) -> bool:
    """Report group squad usage to Stripe"""
    timestamp: int = int(datetime_utils.get_utc_timestamp())
    authors: int = await _get_subscription_usage(
        subscription=subscription,
    )
    result = stripe.SubscriptionItem.create_usage_record(
        subscription.items["squad"],
        quantity=authors,
        timestamp=timestamp,
        action="set",
    )
    return isinstance(result.id, str)


async def update_subscription(
    *,
    subscription: Subscription,
    upgrade: bool,
) -> bool:
    """Upgrade or downgrade a subscription"""
    prices: Dict[str, Price] = await get_prices()
    data: Dict[str, Any] = {
        "items": [],
        "metadata": {"subscription": ""},
    }
    result: bool = True

    if upgrade:
        data["items"] = [
            {
                "price": prices["squad"].id,
                "metadata": {
                    "group": subscription.group,
                    "name": "squad",
                    "organization": subscription.organization,
                },
            }
        ]
        data["metadata"]["subscription"] = "squad"
    else:
        data["items"] = [
            {
                "id": subscription.items["squad"],
                "clear_usage": True,
                "deleted": True,
            },
        ]
        data["metadata"]["subscription"] = "machine"

        # Pay squad authors to date
        result = await _pay_squad_authors_to_date(
            prices=prices,
            subscription=subscription,
        )

        # Raise exception if payment intent failed
        if not result:
            raise CouldNotDowngradeSubscription()

    # Update subscription
    result = (
        result
        and stripe.Subscription.modify(
            subscription.id,
            **data,
        ).status
        == "active"
    )

    return result


async def get_authors_data(
    *, date: datetime, group: str
) -> List[Dict[str, str]]:
    expected_columns: Dict[str, List[str]] = {
        "actor": ["actor"],
        "groups": ["groups"],
        "commit": ["commit", "sha1"],
        "repository": ["repository"],
    }
    buffer: io.BytesIO = await _get_billing_buffer(date=date, group=group)
    buffer_str: io.StringIO = io.StringIO(buffer.read().decode())

    return [
        {
            column: next(value_generator, "-")
            for column, possible_names in expected_columns.items()
            for value_generator in [
                # This attempts to get the column value by trying the
                # possible names the column may have
                # this only yields truthy values (values with data)
                filter(None, (row.get(name) for name in possible_names)),
            ]
        }
        for row in csv.DictReader(buffer_str)
    ]
