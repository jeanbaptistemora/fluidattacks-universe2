from typing import (
    Dict,
    NamedTuple,
    Optional,
)


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
    items: Dict[str, str]
