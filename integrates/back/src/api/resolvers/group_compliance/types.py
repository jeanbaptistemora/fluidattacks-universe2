from api.resolvers.types import (
    Requirement,
)
from typing import (
    NamedTuple,
)


class GroupUnfulfilledStandard(NamedTuple):
    standard_id: str
    title: str
    unfulfilled_requirements: list[Requirement]
