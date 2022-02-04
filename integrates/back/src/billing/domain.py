from aioextensions import (
    collect,
)
from billing import (
    dal,
)
from billing.types import (
    Customer,
    PaymentMethod,
    Subscription,
)
from custom_exceptions import (
    BillingCustomerHasActiveSubscription,
    BillingCustomerHasNoPaymentMethod,
    BillingSubscriptionSameActive,
    CouldNotActivateSubscription,
    CouldNotCreatePaymentMethod,
    InvalidBillingCustomer,
    InvalidBillingPaymentMethod,
)
from dataloaders import (
    get_new_context,
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


async def _group_has_active_subscription(
    *,
    group_name: str,
    org_billing_customer: str,
) -> bool:
    """True if group has active subscription"""
    subs: Dict[str, Subscription] = await dal.get_group_subscriptions(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
        limit=1000,
    )
    return len(subs) > 0


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
) -> Dict[str, Any]:
    """Format create subscription session data according to stripe API"""
    billing_cycle_anchor: int = int(
        datetime_utils.get_first_day_next_month_timestamp()
    )
    items: List[Dict[str, Any]] = [
        {
            "price": (
                await dal.get_price(
                    subscription=subscription,
                    active=True,
                )
            ).id,
        },
    ]
    if subscription == "machine":
        items[0]["quantity"] = 1

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


async def _create_subscription(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
) -> bool:
    """Helper for creating Stripe subscription"""
    # Raise exception if customer does not have a payment method
    if not await _customer_has_payment_method(
        org_billing_customer=org_billing_customer,
    ):
        raise BillingCustomerHasNoPaymentMethod()

    # machine+squad if subscription is squad
    subs: List[str] = [subscription]
    if subscription == "squad":
        subs.append("machine")

    # Format subs data
    data: Dict[str, Dict[str, Any]] = {
        sub: await _format_create_subscription_data(
            subscription=sub,
            org_billing_customer=org_billing_customer,
            org_name=org_name,
            group_name=group_name,
        )
        for sub in subs
    }

    # Create machine subs
    result: bool = await dal.create_subscription(**data["machine"])

    # Raise exception if machine could not be activated
    if not result:
        raise CouldNotActivateSubscription()

    if subscription == "squad":
        result = result and await dal.create_subscription(**data["squad"])

    return result


async def _update_subscription(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
    subscriptions: Dict[str, Subscription],
) -> bool:
    """Helper for updating a Stripe subscription"""
    # Raise exception if customer does not have a payment method
    if not await _customer_has_payment_method(
        org_billing_customer=org_billing_customer,
    ):
        raise BillingCustomerHasNoPaymentMethod()

    # Report usage if subscription is squad
    if "squad" in subscriptions.keys():
        await dal.report_subscription_usage(
            subscription=subscriptions["squad"],
        )

    if subscription == "squad":
        data: Dict[str, Any] = await _format_create_subscription_data(
            subscription=subscription,
            org_billing_customer=org_billing_customer,
            org_name=org_name,
            group_name=group_name,
        )
        return await dal.create_subscription(**data)
    return await dal.remove_subscription(
        subscription_id=subscriptions["squad"].id,
        invoice_now=True,
        prorate=True,
    )


async def _remove_subscription(
    *,
    subscriptions: Dict[str, Subscription],
) -> bool:
    """Helper for cancelling a stripe subscription"""

    # Report usage if subscription is squad
    report: bool = True
    if "squad" in subscriptions.keys():
        report = await dal.report_subscription_usage(
            subscription=subscriptions["squad"],
        )

    return report and all(
        await collect(
            [
                dal.remove_subscription(
                    subscription_id=sub.id,
                    invoice_now=sub.type == "squad",
                    prorate=True,
                )
                for sub in subscriptions.values()
            ]
        )
    )


async def _remove_incomplete_subscriptions(
    *,
    org_billing_customer: str,
    group_name: str,
) -> bool:
    """Cancel all incomplete subscriptions for a group"""
    subscriptions: Dict[str, Subscription] = await dal.get_group_subscriptions(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="incomplete",
        limit=1000,
    )

    return await _remove_subscription(
        subscriptions=subscriptions,
    )


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

    subscriptions: Dict[str, Subscription] = await dal.get_group_subscriptions(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
        limit=1000,
    )

    # Raise exception if group already has the same subscription active
    already_free: bool = subscription == "free" and len(subscriptions) == 0
    already_machine: bool = (
        subscription == "machine" and len(subscriptions) == 1
    )
    already_squad: bool = subscription == "squad" and len(subscriptions) == 2
    if already_free or already_machine or already_squad:
        raise BillingSubscriptionSameActive()

    # Remove incomplete subscriptions
    result: bool = await _remove_incomplete_subscriptions(
        org_billing_customer=org_billing_customer,
        group_name=group_name,
    )

    if subscription == "free":
        result = result and await _remove_subscription(
            subscriptions=subscriptions,
        )
    elif len(subscriptions) > 0:
        result = result and await _update_subscription(
            subscription=subscription,
            org_billing_customer=org_billing_customer,
            org_name=org_name,
            group_name=group_name,
            subscriptions=subscriptions,
        )
    else:
        result = result and await _create_subscription(
            subscription=subscription,
            org_billing_customer=org_billing_customer,
            org_name=org_name,
            group_name=group_name,
        )

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
        payment_method: PaymentMethod = await dal.create_payment_method(
            card_number=card_number,
            card_expiration_month=card_expiration_month,
            card_expiration_year=card_expiration_year,
            card_cvc=card_cvc,
            default=make_default,
        )

        # Attach payment method to customer
        result: bool = await dal.attach_payment_method(
            payment_method_id=payment_method.id,
            org_billing_customer=customer.id,
        )
    except CardError as ex:
        raise CouldNotCreatePaymentMethod() from ex

    # If payment method is the first one registered or selected as default,
    # then make it default
    if not customer.default_payment_method or make_default:
        await dal.update_default_payment_method(
            payment_method_id=payment_method.id,
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

    subscriptions: Dict[
        str, Subscription
    ] = await dal.get_customer_subscriptions(
        org_billing_customer=org_billing_customer,
        limit=1000,
        status="active",
    )

    # Raise exception if payment method is the last one
    # and there are active subscriptions
    if len(payment_methods) == 1 and len(subscriptions) > 0:
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
        if event.type in (
            "customer.subscription.created",
            "customer.subscription.deleted",
        ):
            tier: str = ""
            subs: Dict[str, Subscription] = await dal.get_group_subscriptions(
                group_name=event.data.object.metadata.group,
                org_billing_customer=event.data.object.customer,
                status="active",
                limit=1000,
            )

            if (
                event.type == "customer.subscription.deleted"
                and event.data.object.metadata.subscription == "machine"
            ):
                tier = "free"
            elif "squad" in subs.keys():
                tier = "squad"
            elif "machine" in subs.keys():
                tier = "machine"

            if await groups_domain.update_group_tier(
                loaders=get_new_context(),
                reason=f"Update triggered by Stripe with event {event.id}",
                requester_email="development@fluidattacks.com",
                group_name=event.data.object.metadata.group,
                tier=tier,
            ):
                message = "Success"
        else:
            message = f"Unhandled event type: {event.type}"
            status = "failed"
            LOGGER.warning(message, extra=dict(extra=locals()))
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
