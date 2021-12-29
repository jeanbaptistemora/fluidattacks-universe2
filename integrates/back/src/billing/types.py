from typing import (
    NamedTuple,
)


class Checkout(NamedTuple):
    cancel_url: str
    success_url: str
    payment_url: str


class Portal(NamedTuple):
    group: str
    portal_url: str
    return_url: str
