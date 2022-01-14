from typing import (
    List,
    NamedTuple,
)


class AddBillingSubscriptionPayload(NamedTuple):
    id: str
    cancel_url: str
    success: bool
    success_url: str
    payment_url: str


class Customer(NamedTuple):
    id: str
    name: str
    email: str


class Price(NamedTuple):
    id: str
    subscription: str


class Portal(NamedTuple):
    organization: str
    portal_url: str
    return_url: str


class SubscriptionItem(NamedTuple):
    id: str
    type: str


class Subscription(NamedTuple):
    id: str
    group: str
    org_billing_customer: str
    organization: str
    type: str
    items: List[SubscriptionItem]


class UpdateBillingSubscriptionPayload(NamedTuple):
    amount_due: int
    amount_paid: int
    amount_remaining: int
    success: bool
