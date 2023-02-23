from db_model.groups.enums import (
    GroupTier,
)
from db_model.organizations.types import (
    DocumentFile,
)
from typing import (
    NamedTuple,
)


class GroupAuthor(NamedTuple):
    actor: str
    commit: str | None
    groups: frozenset[str]
    organization: str | None
    repository: str | None


class GroupBilling(NamedTuple):
    authors: tuple[GroupAuthor, ...]
    costs_authors: int
    costs_base: int
    costs_total: int
    number_authors: int


class OrganizationActiveGroup(NamedTuple):
    name: str
    tier: GroupTier


class OrganizationAuthor(NamedTuple):
    actor: str
    active_groups: tuple[OrganizationActiveGroup, ...]


class OrganizationBilling(NamedTuple):
    authors: tuple[OrganizationAuthor, ...]
    costs_authors: int
    costs_base: int
    costs_total: int
    number_authors_machine: int
    number_authors_squad: int
    number_authors_total: int
    number_groups_machine: int
    number_groups_squad: int
    number_groups_total: int
    organization: str


class Address(NamedTuple):
    line_1: str
    line_2: str | None
    city: str
    state: str | None
    country: str
    postal_code: str


class Customer(NamedTuple):
    id: str
    name: str
    address: Address | None
    email: str
    phone: str | None
    default_payment_method: str | None


class PaymentMethod(NamedTuple):
    id: str
    fingerprint: str
    last_four_digits: str
    expiration_month: str
    expiration_year: str
    brand: str
    default: bool
    business_name: str
    city: str
    country: str
    email: str
    state: str
    rut: DocumentFile | None
    tax_id: DocumentFile | None


class Price(NamedTuple):
    id: str
    currency: str
    amount: int


class Subscription(NamedTuple):
    id: str
    group: str
    org_billing_customer: str
    organization: str
    status: str
    type: str
    items: dict[str, str]
