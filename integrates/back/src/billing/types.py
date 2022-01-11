from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
)


class Customer(NamedTuple):
    id: str
    name: str
    email: str


class Invoice(NamedTuple):
    account_name: str
    amount_due: int
    amount_paid: int
    amount_remaining: int
    data: List[Dict[str, Any]]


class Price(NamedTuple):
    id: str
    subscription: str
    metered: bool


class Portal(NamedTuple):
    organization: str
    portal_url: str
    return_url: str


class Subscription(NamedTuple):
    id: str
    group: str
    org_billing_customer: str
    organization: str
    type: str
    items: List[str]
