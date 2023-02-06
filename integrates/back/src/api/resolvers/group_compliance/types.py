from typing import (
    NamedTuple,
)


class Requirement(NamedTuple):
    id: str
    title: str


class GroupUnfulfilledStandard(NamedTuple):
    standard_id: str
    title: str
    unfulfilled_requirements: list[Requirement]
