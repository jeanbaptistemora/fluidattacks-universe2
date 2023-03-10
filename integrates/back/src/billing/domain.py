# pylint: disable=too-many-locals
# pylint:disable=too-many-lines

from aioextensions import (
    collect,
)
from billing import (
    dal,
)
from billing.types import (
    Customer,
    GroupAuthor,
    GroupBilling,
    OrganizationActiveGroup,
    OrganizationAuthor,
    OrganizationBilling,
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
    InvalidExpiryDateField,
    InvalidFileSize,
    InvalidFileType,
    NoActiveBillingSubscription,
    PaymentMethodAlreadyExists,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    organizations as organizations_model,
)
from db_model.groups.enums import (
    GroupTier,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    DocumentFile,
    Organization,
    OrganizationDocuments,
    OrganizationMetadataToUpdate,
    OrganizationPaymentMethods,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
import logging
import logging.config
from more_itertools import (
    flatten,
)
from newutils import (
    datetime as datetime_utils,
    files as files_utils,
    validations,
)
from notifications import (
    domain as notifications_domain,
)
from s3 import (
    operations as s3_ops,
)
from settings import (
    LOGGING,
)
from starlette.datastructures import (
    UploadFile,
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
)
import uuid

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
TRIAL_DAYS: int = 14


async def save_file(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        file_object,
        f"resources/{file_name}",
    )


async def search_file(file_name: str) -> list[str]:
    return await s3_ops.list_files(
        f"resources/{file_name}",
    )


async def remove_file(file_name: str) -> None:
    await s3_ops.remove_file(
        f"resources/{file_name}",
    )


async def get_document_link(
    org: Organization, payment_id: str, file_name: str
) -> str:
    org_name = org.name.lower()
    payment_method: list[OrganizationPaymentMethods] = []
    file_url = ""
    if org.payment_methods:
        payment_method = list(
            filter(lambda method: method.id == payment_id, org.payment_methods)
        )
        if len(payment_method) == 0:
            raise InvalidBillingPaymentMethod()
        business_name = payment_method[0].business_name.lower()
        file_url = f"billing/{org_name}/{business_name}/{file_name}"

    return await s3_ops.sign_url(
        f"resources/{file_url}",
        10,
    )


def _customer_has_payment_method(
    *,
    org_billing_customer: str,
) -> bool:
    customer: Customer = dal.get_customer(
        org_billing_customer=org_billing_customer,
    )
    return customer.default_payment_method is not None


def _format_create_subscription_data(
    *,
    subscription: str,
    org_billing_customer: str,
    org_name: str,
    group_name: str,
    trial: bool,
) -> dict[str, Any]:
    """Format create subscription session data according to stripe API"""
    prices: dict[str, Price] = dal.get_prices()
    now: datetime = datetime_utils.get_utc_now()

    result: dict[str, Any] = {
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


def _has_subscription(
    *,
    statuses: list[str],
    subscriptions: list[Subscription],
) -> bool:
    for subscription in subscriptions:
        if subscription.status in statuses:
            return True
    return False


def _get_active_subscription(
    *,
    subscriptions: list[Subscription],
) -> Subscription | None:
    result: list[Subscription] = [
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
    org_billing_customer: str | None,
    org_name: str,
    group_name: str,
) -> bool:
    """Update a subscription for a group"""
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    # Raise exception if customer does not have a payment method
    if not _customer_has_payment_method(
        org_billing_customer=org_billing_customer,
    ):
        raise BillingCustomerHasNoPaymentMethod()

    subscriptions: list[Subscription] = dal.get_group_subscriptions(
        group_name=group_name,
        org_billing_customer=org_billing_customer,
        status="all",
    )

    # Raise exception if group has incomplete, past_due or unpaid subscriptions
    if _has_subscription(
        statuses=["incomplete", "past_due", "unpaid"],
        subscriptions=subscriptions,
    ):
        raise CouldNotUpdateSubscription()

    current: Subscription | None = _get_active_subscription(
        subscriptions=subscriptions
    )

    # Raise exception if group already has the same subscription active
    is_free: bool = current is None and subscription == "free"
    is_other: bool = current is not None and current.type == subscription
    if is_free or is_other:
        raise BillingSubscriptionSameActive()

    result: bool = False
    if current is None:
        trial: bool = not _has_subscription(
            statuses=["canceled"],
            subscriptions=subscriptions,
        )
        data: dict[str, Any] = _format_create_subscription_data(
            subscription=subscription,
            org_billing_customer=org_billing_customer,
            org_name=org_name,
            group_name=group_name,
            trial=trial,
        )
        result = dal.create_subscription(**data)
    elif subscription != "free":
        result = await dal.update_subscription(
            subscription=current,
            upgrade=current.type == "machine" and subscription == "squad",
        )
    else:
        result = dal.remove_subscription(
            subscription_id=current.id,
            invoice_now=current.type == "squad",
            prorate=True,
        )

    if not result:
        raise CouldNotUpdateSubscription()
    return result


def get_customer(
    *,
    org_billing_customer: str,
) -> Customer:
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    return dal.get_customer(
        org_billing_customer=org_billing_customer,
    )


def customer_payment_methods(
    *,
    org: Organization,
    limit: int = 100,
) -> list[PaymentMethod]:
    """Return list of customer's payment methods"""
    # Return empty list if stripe customer does not exist
    payment_methods = []

    if org.billing_customer is not None:
        customer: Customer = dal.get_customer(
            org_billing_customer=org.billing_customer,
        )
        stripe_payment_methods: list[
            dict[str, Any]
        ] = dal.get_customer_payment_methods(
            org_billing_customer=org.billing_customer,
            limit=limit,
        )

        payment_methods += [
            PaymentMethod(
                id=payment_method["id"],
                fingerprint=payment_method["card"]["fingerprint"],
                last_four_digits=payment_method["card"]["last4"],
                expiration_month=str(payment_method["card"]["exp_month"]),
                expiration_year=str(payment_method["card"]["exp_year"]),
                brand=payment_method["card"]["brand"],
                default=payment_method["id"]
                == customer.default_payment_method,
                business_name="",
                city="",
                country="",
                email="",
                state="",
                rut=None,
                tax_id=None,
            )
            for payment_method in stripe_payment_methods
        ]

    if org.payment_methods is not None:
        other_payment_methods: list[
            OrganizationPaymentMethods
        ] = org.payment_methods

        payment_methods += [
            PaymentMethod(
                id=other_method.id,
                fingerprint="",
                last_four_digits="",
                expiration_month="",
                expiration_year="",
                brand="",
                default=False,
                business_name=other_method.business_name,
                city=other_method.city,
                country=other_method.country,
                email=other_method.email,
                state=other_method.state,
                rut=DocumentFile(
                    file_name=other_method.documents.rut.file_name,
                    modified_date=other_method.documents.rut.modified_date,
                )
                if other_method.documents.rut
                else None,
                tax_id=DocumentFile(
                    file_name=other_method.documents.tax_id.file_name,
                    modified_date=other_method.documents.tax_id.modified_date,
                )
                if other_method.documents.tax_id
                else None,
            )
            for other_method in other_payment_methods
        ]

    return payment_methods


async def customer_portal(
    *,
    org_id: str,
    org_name: str,
    user_email: str,
    org_billing_customer: str | None,
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

    return dal.get_customer_portal(
        org_billing_customer=org_billing_customer,
        org_name=org_name,
    )


@validations.validate_file_name_deco("file.filename")
@validations.validate_fields_deco(["file.content_type"])
async def validate_file(file: UploadFile) -> None:
    mib = 1048576
    allowed_mimes = [
        "image/gif",
        "image/jpeg",
        "image/png",
        "application/pdf",
    ]
    if not await files_utils.assert_uploaded_file_mime(file, allowed_mimes):
        raise InvalidFileType("TAX_ID")

    if await files_utils.get_file_size(file) > 10 * mib:
        raise InvalidFileSize()


async def create_billing_customer(
    org: Organization,
    user_email: str,
) -> Customer:
    customer: Customer | None = None
    billing_customer = org.billing_customer
    if billing_customer is None:
        customer = await dal.create_customer(
            org_id=org.id,
            org_name=org.name,
            user_email=user_email,
        )
    else:
        customer = dal.get_customer(
            org_billing_customer=billing_customer,
        )

    return customer


async def validate_legal_document(
    rut: UploadFile | None, tax_id: UploadFile | None
) -> None:
    if rut:
        await validate_file(file=rut)
    if tax_id:
        await validate_file(file=tax_id)


def document_extension(document: UploadFile) -> str:
    extension = {
        "image/gif": ".gif",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf",
        "application/zip": ".zip",
        "text/csv": ".csv",
        "text/plain": ".txt",
    }.get(document.content_type, "")

    return extension


@validations.validate_field_length_deco("business_name", 60)
@validations.validate_fields_deco(["business_name", "email"])
async def update_documents(
    *,
    org: Organization,
    payment_method_id: str,
    business_name: str,
    city: str,
    country: str,
    email: str,
    state: str,
    rut: UploadFile | None = None,
    tax_id: UploadFile | None = None,
) -> bool:

    documents = OrganizationDocuments()
    org_name = org.name.lower()
    business_name = business_name.lower()

    if org.payment_methods:
        actual_payment_method = list(
            filter(
                lambda method: method.id == payment_method_id,
                org.payment_methods,
            )
        )[0]
        if actual_payment_method.business_name.lower() != business_name:
            document_prefix = (
                f"billing/{org.name.lower()}/"
                + f"{actual_payment_method.business_name.lower()}"
            )
            file_name: str = ""
            if actual_payment_method.documents.rut:
                file_name = actual_payment_method.documents.rut.file_name
            if actual_payment_method.documents.tax_id:
                file_name = actual_payment_method.documents.tax_id.file_name

            await remove_file(f"{document_prefix}/{file_name}")

    if rut:
        rut_file_name = f"{org_name}-{business_name}{document_extension(rut)}"
        rut_full_name = f"billing/{org_name}/{business_name}/{rut_file_name}"
        validations.validate_sanitized_csv_input(
            rut.filename, rut.content_type, rut_full_name
        )
        await save_file(rut, rut_full_name)
        documents = OrganizationDocuments(
            rut=DocumentFile(
                file_name=rut_file_name,
                modified_date=datetime_utils.get_utc_now(),
            )
        )
    if tax_id:
        tax_id_file_name = (
            f"{org_name}-{business_name}{document_extension(tax_id)}"
        )
        tax_id_full_name = (
            f"billing/{org_name}/{business_name}/{tax_id_file_name}"
        )
        validations.validate_sanitized_csv_input(
            tax_id.filename, tax_id.content_type, tax_id_full_name
        )
        await save_file(tax_id, tax_id_full_name)
        documents = OrganizationDocuments(
            tax_id=DocumentFile(
                file_name=tax_id_file_name,
                modified_date=datetime_utils.get_utc_now(),
            )
        )

    return await update_other_payment_method(
        org=org,
        documents=documents,
        payment_method_id=payment_method_id,
        business_name=business_name,
        city=city,
        country=country,
        email=email,
        state=state,
    )


async def create_credit_card_payment_method(
    *,
    org: Organization,
    user_email: str,
    card_number: str,
    card_expiration_month: str,
    card_expiration_year: str,
    card_cvc: str,
    make_default: bool,
) -> bool:
    """Create a credit card payment method and associate it to the customer"""

    # Create customer if it does not exist
    customer = await create_billing_customer(org, user_email)

    result: bool = False
    # get actual payment methods
    payment_methods: list[PaymentMethod] = customer_payment_methods(
        org=org,
        limit=1000,
    )
    try:
        created: PaymentMethod = dal.create_payment_method(
            card_number=card_number,
            card_expiration_month=card_expiration_month,
            card_expiration_year=card_expiration_year,
            card_cvc=card_cvc,
            default=make_default,
        )

        # Raise exception if payment method already exists for customer
        if created.fingerprint in [
            payment_method.fingerprint for payment_method in payment_methods
        ]:
            raise PaymentMethodAlreadyExists()

        # Attach payment method to customer
        result = dal.attach_payment_method(
            payment_method_id=created.id,
            org_billing_customer=customer.id,
        )
    except CardError as ex:
        raise CouldNotCreatePaymentMethod() from ex

    # If payment method is the first one registered or selected as default,
    # then make it default
    if not customer.default_payment_method or make_default:
        dal.update_default_payment_method(
            payment_method_id=created.id,
            org_billing_customer=customer.id,
        )

    return result


@validations.validate_field_length_deco("business_name", limit=60)
@validations.validate_fields_deco(["business_name"])
async def create_other_payment_method(
    *,
    org: Organization,
    user_email: str,
    business_name: str,
    city: str,
    country: str,
    email: str,
    state: str,
    rut: UploadFile | None = None,
    tax_id: UploadFile | None = None,
) -> bool:
    """Create other payment method and associate it to the organization"""
    if rut:
        validations.validate_sanitized_csv_input(
            rut.filename, rut.content_type
        )
    if tax_id:
        validations.validate_sanitized_csv_input(
            tax_id.filename, tax_id.content_type
        )
    await validate_legal_document(rut, tax_id)

    other_payment_id = str(uuid.uuid4())
    other_payment = OrganizationPaymentMethods(
        business_name=business_name,
        city=city,
        country=country,
        documents=OrganizationDocuments(),
        email=email,
        id=other_payment_id,
        state=state,
    )

    # Raise exception if payment method already exists for organization
    if org.payment_methods:
        if business_name in [
            payment_method.business_name
            for payment_method in org.payment_methods
        ]:
            raise PaymentMethodAlreadyExists()
        org.payment_methods.append(other_payment)
    else:
        org = org._replace(
            payment_methods=[other_payment],
        )
    await organizations_model.update_metadata(
        metadata=OrganizationMetadataToUpdate(
            payment_methods=org.payment_methods
        ),
        organization_id=org.id,
        organization_name=org.name,
    )
    await notifications_domain.request_other_payment_methods(
        business_legal_name=business_name,
        city=city,
        country=country,
        efactura_email=email,
        rut=rut,
        tax_id=tax_id,
        user_email=user_email,
    )
    return await update_documents(
        org=org,
        payment_method_id=other_payment_id,
        business_name=business_name,
        city=city,
        country=country,
        email=email,
        state=state,
        rut=rut,
        tax_id=tax_id,
    )


def update_credit_card_payment_method(
    *,
    org: Organization,
    payment_method_id: str,
    card_expiration_month: int,
    card_expiration_year: int,
    make_default: bool,
) -> bool:
    if not isinstance(card_expiration_month, int) and not isinstance(
        card_expiration_year, int
    ):
        raise InvalidExpiryDateField()

    # Raise exception if stripe customer does not exist
    if org.billing_customer is None:
        raise InvalidBillingCustomer()

    # Raise exception if payment method does not belong to organization
    payment_methods: list[PaymentMethod] = customer_payment_methods(
        org=org,
        limit=1000,
    )
    if payment_method_id not in [
        payment_method.id for payment_method in list(payment_methods)
    ]:
        raise InvalidBillingPaymentMethod()

    result: bool = dal.update_payment_method(
        payment_method_id=payment_method_id,
        card_expiration_month=card_expiration_month,
        card_expiration_year=card_expiration_year,
    )
    if make_default:
        result = result and dal.update_default_payment_method(
            payment_method_id=payment_method_id,
            org_billing_customer=org.billing_customer,
        )

    return result


@validations.validate_field_length_deco("business_name", 60)
@validations.validate_fields_deco(["business_name"])
async def update_other_payment_method(
    *,
    org: Organization,
    documents: OrganizationDocuments,
    payment_method_id: str,
    business_name: str,
    city: str,
    country: str,
    email: str,
    state: str,
) -> bool:
    # Raise exception if payment method does not belong to organization
    payment_methods: list[PaymentMethod] = customer_payment_methods(
        org=org,
        limit=1000,
    )
    if payment_method_id not in [
        payment_method.id for payment_method in list(payment_methods)
    ]:
        raise InvalidBillingPaymentMethod()

    # get actual payment methods
    other_payment_methods: list[OrganizationPaymentMethods] = []
    if org.payment_methods:
        other_payment_methods = org.payment_methods

    other_payment_methods = list(
        filter(
            lambda method: method.id != payment_method_id,
            other_payment_methods,
        )
    )
    other_payment_methods.append(
        OrganizationPaymentMethods(
            business_name=business_name,
            city=city,
            country=country,
            documents=documents,
            email=email,
            id=payment_method_id,
            state=state,
        )
    )
    await organizations_model.update_metadata(
        metadata=OrganizationMetadataToUpdate(
            payment_methods=other_payment_methods
        ),
        organization_id=org.id,
        organization_name=org.name,
    )
    return True


def _set_default_payment(
    payment_methods: list[PaymentMethod],
    payment_method_id: str,
    org: Organization,
) -> bool:
    # Set another payment method as default
    # if current credit card default will be deleted
    result: bool = True
    default: PaymentMethod = [
        payment_method
        for payment_method in payment_methods
        if payment_method.default
    ][0]
    credit_card_payment_methods = [
        credit_card_payment
        for credit_card_payment in payment_methods
        if credit_card_payment.last_four_digits
    ]
    if (
        len(credit_card_payment_methods) > 1
        and payment_method_id == default.id
    ):
        non_defaults = [
            payment_method
            for payment_method in payment_methods
            if not payment_method.default
        ]

        result = dal.update_default_payment_method(
            payment_method_id=non_defaults[0].id,
            org_billing_customer=org.billing_customer,
        )

    return result


async def remove_payment_method(
    *,
    org: Organization,
    payment_method_id: str,
) -> bool:
    # Raise exception if stripe customer does not exist
    if org.billing_customer is None:
        raise InvalidBillingCustomer()

    payment_methods: list[PaymentMethod] = customer_payment_methods(
        org=org,
        limit=1000,
    )

    # Raise exception if payment method does not belong to organization
    if payment_method_id not in [
        payment_method.id for payment_method in payment_methods
    ]:
        raise InvalidBillingPaymentMethod()

    if (
        list(
            filter(
                lambda method: method.id == payment_method_id, payment_methods
            )
        )[0].last_four_digits
        == ""
    ):
        # get actual payment methods
        other_payment_methods: list[OrganizationPaymentMethods] = []
        if org.payment_methods:
            other_payment_methods = org.payment_methods

        payment_method = list(
            filter(
                lambda method: method.id == payment_method_id,
                other_payment_methods,
            )
        )[0]
        business_name = payment_method.business_name
        other_payment_methods = list(
            filter(
                lambda method: method.id != payment_method_id,
                other_payment_methods,
            )
        )
        await organizations_model.update_metadata(
            metadata=OrganizationMetadataToUpdate(
                payment_methods=other_payment_methods
            ),
            organization_id=org.id,
            organization_name=org.name,
        )
        document_prefix = f"billing/{org.name.lower()}/{business_name.lower()}"
        file_name: str = ""
        if payment_method.documents.rut:
            file_name = payment_method.documents.rut.file_name
        if payment_method.documents.tax_id:
            file_name = payment_method.documents.tax_id.file_name

        await remove_file(f"{document_prefix}/{file_name}")

        return True

    subscriptions: list[Subscription] = dal.get_customer_subscriptions(
        org_billing_customer=org.billing_customer,
        limit=1000,
        status="",
    )

    # Raise exception if payment method is the last one
    # and there are active or trialing subscriptions
    if len(payment_methods) == 1 and _has_subscription(
        statuses=["active", "trialing"], subscriptions=subscriptions
    ):
        raise BillingCustomerHasActiveSubscription()

    update_default_payment = _set_default_payment(
        payment_methods, payment_method_id, org
    )
    result = update_default_payment and dal.remove_payment_method(
        payment_method_id=payment_method_id,
    )

    return result


async def report_subscription_usage(
    *,
    group_name: str,
    org_billing_customer: str,
) -> bool:
    """Report group squad usage to Stripe"""
    subscriptions: list[Subscription] = dal.get_group_subscriptions(
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


async def get_group_billing(
    *, date: datetime, org: Organization, group: Group, loaders: Dataloaders
) -> GroupBilling:
    group_authors: tuple[GroupAuthor, ...] = await dal.get_group_authors(
        date=date,
        group=group.name,
    )
    number_authors: int = len(group_authors)

    prices: dict[str, Price] = get_prices()
    org_authors: dict[str, OrganizationAuthor] = {
        author.actor: author
        for author in await get_organization_authors(
            date=date,
            org=org,
            loaders=loaders,
        )
    }
    group_squad_authors: tuple[GroupAuthor, ...] = tuple(
        author
        for author in group_authors
        if GroupTier.SQUAD
        in tuple(
            group.tier for group in org_authors[author.actor].active_groups
        )
    )
    costs_authors: int = int(
        sum(
            tuple(
                prices["squad"].amount
                / len(
                    tuple(
                        group
                        for group in org_authors[
                            squad_author.actor
                        ].active_groups
                        if group.tier == GroupTier.SQUAD
                    )
                )
                for squad_author in group_squad_authors
            )
        )
        / 100
    )
    costs_base: int = (
        int(prices["machine"].amount / 100)
        if group.state.tier in (GroupTier.SQUAD, GroupTier.MACHINE)
        else 0
    )
    costs_total: int = costs_base + costs_authors

    return GroupBilling(
        authors=group_authors,
        costs_authors=costs_authors,
        costs_base=costs_base,
        costs_total=costs_total,
        number_authors=number_authors,
    )


async def get_organization_authors(
    *,
    date: datetime,
    org: Organization,
    loaders: Dataloaders,
) -> tuple[OrganizationAuthor, ...]:
    org_groups: dict[str, Group] = {
        group.name: group
        for group in await loaders.organization_groups.load(
            org.id,
        )
    }
    org_authors: tuple[GroupAuthor, ...] = tuple(
        flatten(
            await collect(
                [
                    dal.get_group_authors(date=date, group=group)
                    for group in org_groups
                ],
                workers=10,
            )
        )
    )
    unique_authors: frozenset[str] = frozenset(
        author.actor for author in org_authors
    )
    unique_author_groups: dict[str, frozenset[str]] = {
        unique_author: frozenset(
            flatten(
                chain(
                    tuple(
                        author.groups
                        for author in org_authors
                        if author.actor == unique_author
                    )
                )
            )
        )
        for unique_author in unique_authors
    }
    return tuple(
        OrganizationAuthor(
            actor=actor,
            active_groups=tuple(
                OrganizationActiveGroup(
                    name=group, tier=org_groups[group].state.tier
                )
                for group in groups
            ),
        )
        for actor, groups in unique_author_groups.items()
    )


async def get_organization_billing(
    *,
    date: datetime,
    org: Organization,
    loaders: Dataloaders,
) -> OrganizationBilling:
    groups_total: list[Group] = await loaders.organization_groups.load(org.id)
    groups_machine: frozenset[str] = frozenset(
        group.name
        for group in groups_total
        if group.state.tier == GroupTier.MACHINE
    )
    groups_squad: frozenset[str] = frozenset(
        group.name
        for group in groups_total
        if group.state.tier == GroupTier.SQUAD
    )

    authors_total: tuple[
        OrganizationAuthor, ...
    ] = await get_organization_authors(
        date=date,
        org=org,
        loaders=loaders,
    )
    authors_machine: frozenset[str] = frozenset(
        author.actor
        for author in authors_total
        if bool(
            frozenset(group.name for group in author.active_groups)
            & groups_machine
        )
    )
    authors_squad: frozenset[str] = frozenset(
        author.actor
        for author in authors_total
        if bool(
            frozenset(group.name for group in author.active_groups)
            & groups_squad
        )
    )

    prices: dict[str, Price] = get_prices()
    costs_base: int = int(
        prices["machine"].amount
        * (len(groups_squad) + len(groups_machine))
        / 100
    )
    costs_authors: int = int(len(authors_squad) * prices["squad"].amount / 100)
    costs_total: int = costs_base + costs_authors

    return OrganizationBilling(
        authors=authors_total,
        costs_authors=costs_authors,
        costs_base=costs_base,
        costs_total=costs_total,
        number_authors_machine=len(authors_machine),
        number_authors_squad=len(authors_squad),
        number_authors_total=len(authors_total),
        number_groups_machine=len(groups_machine),
        number_groups_squad=len(groups_squad),
        number_groups_total=len(groups_total),
        organization=org.id,
    )


def get_prices() -> dict[str, Price]:
    """Get model prices"""
    return dal.get_prices()


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
            await groups_domain.update_group_tier(
                loaders=get_new_context(),
                comments=f"Triggered by Stripe with event {event.id}",
                group_name=str(event.data.object.metadata.group).lower(),
                tier=GroupTier[tier.upper()],
                email="development@fluidattacks.com",
            )
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
