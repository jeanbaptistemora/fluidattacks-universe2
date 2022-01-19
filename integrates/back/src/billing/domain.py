from aioextensions import (
    collect,
)
from billing import (
    dal,
)
from billing.types import (
    Customer,
    PaymentMethod,
    Portal,
    Subscription,
)
from custom_exceptions import (
    BillingCustomerHasNoPaymentMethod,
    BillingGroupActiveSubscription,
    BillingGroupWithoutSubscription,
    BillingSubscriptionSameActive,
    InvalidBillingCustomer,
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
    subs: Dict[str, Subscription] = await dal.get_subscriptions(
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
    print(customer.default_payment_method)
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


async def customer_payment_methods(
    *, org_billing_customer: str, limit: int = 100
) -> List[PaymentMethod]:
    """Return list of customer's payment methods"""
    return await dal.get_customer_payment_methods(
        org_billing_customer=org_billing_customer,
        limit=limit,
    )


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

    # Create payment method
    payment_method: PaymentMethod = await dal.create_payment_method(
        card_number=card_number,
        card_expiration_month=card_expiration_month,
        card_expiration_year=card_expiration_year,
        card_cvc=card_cvc,
    )

    # Attach payment method to customer
    result: bool = await dal.attach_payment_method(
        payment_method_id=payment_method.id,
        org_billing_customer=customer.id,
    )

    # If payment method is the first one registered or selected as default,
    # then make it default
    if not customer.default_payment_method or make_default:
        await dal.set_default_payment_method(
            payment_method_id=payment_method.id,
            org_billing_customer=customer.id,
        )

    return result


async def create_subscription(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
) -> bool:
    """Create Stripe subscription"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    # Raise exception if group already has an active subscription
    if await _group_has_active_subscription(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
    ):
        raise BillingGroupActiveSubscription()

    # Raise exception if customer does not have a payment method
    if not await _customer_has_payment_method(
        org_billing_customer=org_billing_customer,
    ):
        raise BillingCustomerHasNoPaymentMethod()

    # machine+squad if subscription is squad
    subs: List[str] = [subscription]
    if subscription == "squad":
        subs.append("machine")

    data: List[Dict[str, Any]] = await collect(
        [
            _format_create_subscription_data(
                subscription=sub,
                org_billing_customer=org_billing_customer,
                org_name=org_name,
                group_name=group_name,
            )
            for sub in subs
        ]
    )

    return all(await collect([dal.create_subscription(**sub) for sub in data]))


async def create_portal(
    *,
    org_name: str,
    org_billing_customer: str,
) -> Portal:
    """Create Stripe portal session"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    return await dal.create_portal(
        org_billing_customer=org_billing_customer,
        org_name=org_name,
    )


async def update_subscription(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
) -> bool:
    """Preview a subscription update"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    subs: Dict[str, Subscription] = await dal.get_subscriptions(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
        limit=1000,
    )

    # Raise exception if group does not have an active subscription
    if len(subs) == 0:
        raise BillingGroupWithoutSubscription()

    # Raise exception if group already has the same subscription active
    if (subscription == "machine" and "squad" not in subs.keys()) or (
        subscription == "squad" and "squad" in subs.keys()
    ):
        raise BillingSubscriptionSameActive()

    # Report usage if subscription is squad
    report: bool = True
    if "squad" in subs.keys():
        report = await dal.report_subscription_usage(
            subscription=subs["squad"],
        )

    if subscription == "squad":
        data: Dict[str, Any] = await _format_create_subscription_data(
            subscription=subscription,
            org_billing_customer=org_billing_customer,
            org_name=org_name,
            group_name=group_name,
        )
        return report and await dal.create_subscription(**data)

    return report and await dal.remove_subscription(
        subscription_id=subs["squad"].id,
        invoice_now=True,
        prorate=True,
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

    subs: Dict[str, Subscription] = await dal.get_subscriptions(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="active",
        limit=1000,
    )

    # Raise exception if group does not have an active subscription
    if len(subs) == 0:
        raise BillingGroupWithoutSubscription()

    # Report usage if subscription is squad
    report: bool = True
    if "squad" in subs.keys():
        report = await dal.report_subscription_usage(
            subscription=subs["squad"],
        )

    return report and all(
        await collect(
            [
                dal.remove_subscription(
                    subscription_id=sub.id,
                    invoice_now=sub.type == "squad",
                    prorate=True,
                )
                for sub in subs.values()
            ]
        )
    )


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
