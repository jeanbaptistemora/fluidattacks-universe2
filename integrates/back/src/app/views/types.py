# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
)


class UserAccessInfo(NamedTuple):
    first_name: str
    last_name: str
    user_email: str
