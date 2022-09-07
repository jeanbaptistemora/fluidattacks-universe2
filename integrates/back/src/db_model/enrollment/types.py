# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
    Optional,
)


class Trial(NamedTuple):
    completed: bool
    extension_date: str
    extension_days: int
    start_date: str


class Enrollment(NamedTuple):
    email: str
    enrolled: bool
    trial: Trial


class EnrollmentMetadataToUpdate(NamedTuple):
    enrolled: Optional[bool] = None
    trial: Optional[Trial] = None
