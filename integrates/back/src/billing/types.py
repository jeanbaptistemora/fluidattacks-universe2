from typing import (
    NamedTuple,
)


class Portal(NamedTuple):
    organization: str
    portal_url: str
    return_url: str


class Customer(NamedTuple):
    id: str
    name: str
    email: str


class ClientReference(NamedTuple):
    organization: str
    group: str
