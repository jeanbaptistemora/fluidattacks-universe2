from typing import (
    NamedTuple,
)


class Checkout(NamedTuple):
    cancel_url: str
    success_url: str
    payment_url: str
