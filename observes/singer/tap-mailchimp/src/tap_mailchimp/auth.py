# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from singer_io.singer2.json import (
    JsonObj,
)
from typing import (
    NamedTuple,
)


class Credentials(NamedTuple):
    api_key: str
    dc: str

    def __str__(self) -> str:
        return "__masked__"


def to_credentials(raw: JsonObj) -> Credentials:
    return Credentials(
        api_key=raw["api_key"].to_primitive(str),
        dc=raw["dc"].to_primitive(str),
    )
