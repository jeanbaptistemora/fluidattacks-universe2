from typing import (
    NamedTuple,
)


class Requirement(NamedTuple):
    id: str
    title: str


class GroupUnfulfilledStandard(NamedTuple):
    title: str
    unfulfilled_requirements: list[Requirement]
