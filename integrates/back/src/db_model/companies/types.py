# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
)


class Trial(NamedTuple):
    completed: bool
    extension_date: str
    extension_days: int
    start_date: str


class Company(NamedTuple):
    domain: str
    trial: Trial
