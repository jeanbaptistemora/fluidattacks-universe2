from billing.types import (
    ClientReference,
)
from typing import (
    List,
)


def parse_client_reference(data: str) -> ClientReference:
    separated: List[str] = data.split("/")

    return ClientReference(
        organization=separated[0],
        group=separated[1],
    )
