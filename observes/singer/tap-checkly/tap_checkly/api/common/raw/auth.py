# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class Credentials:
    api_user: str
    api_key: str

    def __str__(self) -> str:
        return "masked api_key"
