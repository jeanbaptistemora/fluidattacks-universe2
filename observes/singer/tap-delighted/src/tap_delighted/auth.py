# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from typing import (
    NamedTuple,
)


class Credentials(NamedTuple):
    api_key: str

    @classmethod
    def new(cls, raw: str) -> Credentials:
        return cls(raw)

    def __str__(self) -> str:
        return "masked api_key"
