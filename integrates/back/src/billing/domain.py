from billing import (
    dal,
)
from billing.types import (
    Customer,
    PaymentMethod,
    Price,
    Subscription,
)
from custom_exceptions import (
    BillingCustomerHasActiveSubscription,
    BillingCustomerHasNoPaymentMethod,
    BillingSubscriptionSameActive,
    CouldNotCreatePaymentMethod,
    CouldNotUpdateSubscription,
    InvalidBillingCustomer,
    InvalidBillingPaymentMethod,
    NoActiveBillingSubscription,
    PaymentMethodAlreadyExists,
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
from settings import (
    LOGGING,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
)
from stripe.error import (
    CardError,
    SignatureVerificationError,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
TRIAL_DAYS: int = 14


async def _customer_has_payment_method(
    *,
    org_billing_customer: str,
) -> bool:
    customer: Customer = await dal.get_customer(
        org_billing_customer=org_billing_customer,
    )
    return customer.default_payment_method is not None


async def _format_create_subscription_data(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
    trial: bool,
) -> Dict[str, Any]:
    """Format create subscription session data according to stripe API"""
    prices: Dict[str, Price] = await dal.get_prices()
    now: datetime = datetime_utils.get_utc_now()

    result: Dict[str, Any] = {
        "customer": org_billing_customer,
        "items": [
            {
                "price": prices["machine"].id,
                "quantity": 1,
                "metadata": {
                    "group": group_name,
                    "name": "machine",
                    "organization": org_name,
                },
            },
        ],
        "metadata": {
            "group": group_name,
            "organization": org_name,
            "subscription": subscription,
        },
    }

    if trial:
        after_trial: datetime = datetime_utils.get_plus_delta(
            now, days=TRIAL_DAYS
        )
        now = after_trial
        result["trial_end"] = int(after_trial.timestamp())

    result["billing_cycle_anchor"] = int(
        datetime_utils.get_first_day_next_month(now).timestamp()
    )

    if subscription == "squad":
        result["items"].append(
            {
                "price": prices["squad"].id,
                "metadata": {
                    "group": group_name,
                    "name": "squad",
                    "organization": org_name,
                },
            },
        )

    return result


async def _has_subscription(
    *,
    statuses: List[str],
    subscriptions: List[Subscription],
) -> bool:
    for subscription in subscriptions:
        if subscription.status in statuses:
            return True
    return False


async def _get_active_subscription(
    *,
    subscriptions: List[Subscription],
) -> Optional[Subscription]:
    result: List[Subscription] = [
        subscription
        for subscription in subscriptions
        if subscription.status in ("active", "trialing")
    ]
    if len(result) > 0:
        return result[0]
    return None


async def update_subscription(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
) -> bool:
    """Update a subscription for a group"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    # Raise exception if customer does not have a payment method
    if not await _customer_has_payment_method(
        org_billing_customer=org_billing_customer,
    ):
        raise BillingCustomerHasNoPaymentMethod()

    subscriptions: List[Subscription] = await dal.get_group_subscriptions(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="all",
    )

    # Raise exception if group has incomplete, past_due or unpaid subscriptions
    if await _has_subscription(
        statuses=["incomplete", "past_due", "unpaid"],
        subscriptions=subscriptions,
    ):
        raise CouldNotUpdateSubscription()

    current: Optional[Subscription] = await _get_active_subscription(
        subscriptions=subscriptions
    )

    # Raise exception if group already has the same subscription active
    is_free: bool = current is None and subscription == "free"
    is_other: bool = current is not None and current.type == subscription
    if is_free or is_other:
        raise BillingSubscriptionSameActive()

    result: bool = False
    if current is None:
        trial: bool = not await _has_subscription(
            statuses=["canceled"],
            subscriptions=subscriptions,
        )
        data: Dict[str, Any] = await _format_create_subscription_data(
            subscription=subscription,
            org_billing_customer=org_billing_customer,
            org_name=org_name,
            group_name=group_name,
            trial=trial,
        )
        result = await dal.create_subscription(**data)
    elif subscription != "free":
        result = await dal.update_subscription(
            subscription=current,
            upgrade=current.type == "machine" and subscription == "squad",
        )
    else:
        result = await dal.remove_subscription(
            subscription_id=current.id,
            invoice_now=current.type == "squad",
            prorate=True,
        )

    if not result:
        raise CouldNotUpdateSubscription()
    return result


async def customer_payment_methods(
    *, org_billing_customer: str, limit: int = 100
) -> List[PaymentMethod]:
    """Return list of customer's payment methods"""
    # Return empty list if stripe customer does not exist
    if org_billing_customer is None:
        return []

    customer: Customer = await dal.get_customer(
        org_billing_customer=org_billing_customer,
    )
    payment_methods: List[
        Dict[str, Any]
    ] = await dal.get_customer_payment_methods(
        org_billing_customer=org_billing_customer,
        limit=limit,
    )

    return [
        PaymentMethod(
            id=payment_method["id"],
            fingerprint=payment_method["card"]["fingerprint"],
            last_four_digits=payment_method["card"]["last4"],
            expiration_month=str(payment_method["card"]["exp_month"]),
            expiration_year=str(payment_method["card"]["exp_year"]),
            brand=payment_method["card"]["brand"],
            default=payment_method["id"] == customer.default_payment_method,
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
        customer = await dal.create_customer(
            org_id=org_id,
            org_name=org_name,
            user_email=user_email,
        )
    else:
        customer = await dal.get_customer(
            org_billing_customer=org_billing_customer,
        )

    try:
        # Create payment method
        created: PaymentMethod = await dal.create_payment_method(
            card_number=card_number,
            card_expiration_month=card_expiration_month,
            card_expiration_year=card_expiration_year,
            card_cvc=card_cvc,
            default=make_default,
        )

        # Raise exception if payment method already exists for customer
        payment_methods: List[PaymentMethod] = await customer_payment_methods(
            org_billing_customer=customer.id,
            limit=1000,
        )
        if created.fingerprint in [
            payment_method.fingerprint for payment_method in payment_methods
        ]:
            raise PaymentMethodAlreadyExists()

        # Attach payment method to customer
        result: bool = await dal.attach_payment_method(
            payment_method_id=created.id,
            org_billing_customer=customer.id,
        )
    except CardError as ex:
        raise CouldNotCreatePaymentMethod() from ex

    # If payment method is the first one registered or selected as default,
    # then make it default
    if not customer.default_payment_method or make_default:
        await dal.update_default_payment_method(
            payment_method_id=created.id,
            org_billing_customer=customer.id,
        )

    return result


async def create_portal(
    *,
    org_id: str,
    org_name: str,
    user_email: str,
    org_billing_customer: Optional[str],
) -> str:
    """Create Stripe portal session"""
    # Create customer if it does not exist
    if org_billing_customer is None:
        customer: Customer = await dal.create_customer(
            org_id=org_id,
            org_name=org_name,
            user_email=user_email,
        )
        org_billing_customer = customer.id

    return await dal.create_portal(
        org_billing_customer=org_billing_customer,
        org_name=org_name,
    )


async def update_payment_method(
    *,
    org_billing_customer: str,
    payment_method_id: str,
    card_expiration_month: str,
    card_expiration_year: str,
) -> bool:
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    # Raise exception if payment method does not belong to organization
    payment_methods: List[PaymentMethod] = await customer_payment_methods(
        org_billing_customer=org_billing_customer,
        limit=1000,
    )
    if payment_method_id not in [
        payment_method.id for payment_method in payment_methods
    ]:
        raise InvalidBillingPaymentMethod()

    return await dal.update_payment_method(
        payment_method_id=payment_method_id,
        card_expiration_month=card_expiration_month,
        card_expiration_year=card_expiration_year,
    )


async def update_default_payment_method(
    *,
    org_billing_customer: str,
    payment_method_id: str,
) -> bool:
    """Update a customer's default payment method"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    payment_methods: List[PaymentMethod] = await customer_payment_methods(
        org_billing_customer=org_billing_customer,
        limit=1000,
    )

    # Raise exception if payment method does not belong to organization
    if payment_method_id not in [
        payment_method.id for payment_method in payment_methods
    ]:
        raise InvalidBillingPaymentMethod()

    return await dal.update_default_payment_method(
        payment_method_id=payment_method_id,
        org_billing_customer=org_billing_customer,
    )


async def remove_payment_method(
    *,
    org_billing_customer: str,
    payment_method_id: str,
) -> bool:
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    payment_methods: List[PaymentMethod] = await customer_payment_methods(
        org_billing_customer=org_billing_customer,
        limit=1000,
    )

    # Raise exception if payment method does not belong to organization
    if payment_method_id not in [
        payment_method.id for payment_method in payment_methods
    ]:
        raise InvalidBillingPaymentMethod()

    subscriptions: List[Subscription] = await dal.get_customer_subscriptions(
        org_billing_customer=org_billing_customer,
        limit=1000,
        status="",
    )

    # Raise exception if payment method is the last one
    # and there are active or trialing subscriptions
    if len(payment_methods) == 1 and await _has_subscription(
        statuses=["active", "trialing"], subscriptions=subscriptions
    ):
        raise BillingCustomerHasActiveSubscription()

    result: bool = True

    # Set another payment method as default if current default will be deleted
    default: PaymentMethod = [
        payment_method
        for payment_method in payment_methods
        if payment_method.default
    ][0]
    if len(payment_methods) > 1 and payment_method_id == default.id:
        non_defaults = [
            payment_method
            for payment_method in payment_methods
            if not payment_method.default
        ]
        result = await update_default_payment_method(
            payment_method_id=non_defaults[0].id,
            org_billing_customer=org_billing_customer,
        )

    result = result and await dal.remove_payment_method(
        payment_method_id=payment_method_id,
    )
    return result


async def report_subscription_usage(
    *,
    group_name: str,
    org_billing_customer: str,
) -> bool:
    """Report group squad usage to Stripe"""
    subscriptions: List[Subscription] = await dal.get_group_subscriptions(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
    )

    # Raise exception if group does not have an active subscription
    if len(subscriptions) == 0:
        raise NoActiveBillingSubscription()

    return await dal.report_subscription_usage(
        subscription=subscriptions[0],
    )


async def get_authors_data(
    *, date: datetime, group: str
) -> List[Dict[str, str]]:
    return await dal.get_authors_data(
        date=date,
        group=group,
    )


async def get_prices() -> Dict[str, Price]:
    """Get model prices"""
    return await dal.get_prices()


async def webhook(request: Request) -> JSONResponse:
    """Parse Stripe webhook request and execute event"""
    message: str = ""
    status: str = "success"

    try:
        # Create stripe webhook event
        event = await dal.create_webhook_event(
            request=request,
        )

        # Main logic
        tier: str = ""
        if event.type in (
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
        ):
            if event.data.object.status in ("active", "trialing"):
                tier = event.data.object.metadata.subscription
            elif event.data.object.status in ("canceled", "unpaid"):
                tier = "free"

        else:
            message = f"Unhandled event type: {event.type}"
            status = "failed"
            LOGGER.warning(message, extra=dict(extra=locals()))

        if tier != "":
            if await groups_domain.update_group_tier(
                loaders=get_new_context(),
                reason=f"Triggered by Stripe with event {event.id}",
                requester_email="development@fluidattacks.com",
                group_name=event.data.object.metadata.group,
                tier=tier,
            ):
                message = "Success"

    except ValueError as ex:
        message = "Invalid payload"
        status = "failed"
        LOGGER.exception(ex, extra=dict(extra=locals()))
    except SignatureVerificationError as ex:
        message = "Invalid signature"
        status = "failed"
        LOGGER.exception(ex, extra=dict(extra=locals()))

    return JSONResponse(
        {
            "status": status,
            "message": message,
        }
    )
