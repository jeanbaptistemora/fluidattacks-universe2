# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.organizations.types import (
    DocumentFile,
)
from typing import (
    NamedTuple,
    Optional,
)


class GroupAuthor(NamedTuple):
    actor: Optional[str]
    commit: Optional[str]
    groups: Optional[str]
    organization: Optional[str]
    repository: Optional[str]


class GroupBilling(NamedTuple):
    current_spend: int
    total: int
    authors: tuple[GroupAuthor, ...]


class OrganizationAuthor(NamedTuple):
    actor: Optional[str]
    groups: frozenset[Optional[str]]


class OrganizationBilling(NamedTuple):
    current_spend: int
    total: int
    authors: tuple[OrganizationAuthor, ...]


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
