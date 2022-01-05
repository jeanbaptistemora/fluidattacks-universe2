from typing import (
    NamedTuple,
)


class Customer(NamedTuple):
    id: str
    name: str
    email: str


class Price(NamedTuple):
    id: str
    tier: str


class Portal(NamedTuple):
    organization: str
    portal_url: str
    return_url: str


class Subscription(NamedTuple):
    id: str
    group: str
    org_billing_customer: str
    organization: str
    tier: str
