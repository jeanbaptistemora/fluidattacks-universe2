from typing import (
    Dict,
    NamedTuple,
    Optional,
)


class Customer(NamedTuple):
    id: str
    name: str
    email: str
    default_payment_method: Optional[str]


class PaymentMethod(NamedTuple):
    id: str
    last_four_digits: str
    expiration_month: str
    expiration_year: str
    brand: str
    default: bool


class Price(NamedTuple):
    id: str
    currency: str
    amount: int
    type: str


class Subscription(NamedTuple):
    id: str
    group: str
    org_billing_customer: str
    organization: str
    status: str
    type: str
    items: Dict[str, str]
