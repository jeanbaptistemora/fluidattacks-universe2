# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from typing import (
    NamedTuple,
)


class Requirement(NamedTuple):
    id: str
    title: str


class GroupUnfulfilledStandard(NamedTuple):
    title: str
    unfulfilled_requirements: list[Requirement]
