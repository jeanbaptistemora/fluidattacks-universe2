# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.groups.enums import (
    GroupTier,
)
from db_model.organizations.types import (
    DocumentFile,
)
from typing import (
    NamedTuple,
    Optional,
)


class GroupAuthor(NamedTuple):
    actor: str
    commit: Optional[str]
    groups: str
    organization: Optional[str]
    repository: Optional[str]


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
    line_2: Optional[str]
    city: str
    state: Optional[str]
    country: str
    postal_code: str


class Customer(NamedTuple):
    id: str
    name: str
    address: Optional[Address]
    email: str
    phone: Optional[str]
    default_payment_method: Optional[str]


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
    rut: Optional[DocumentFile]
    tax_id: Optional[DocumentFile]


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
