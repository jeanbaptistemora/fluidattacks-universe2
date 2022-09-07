# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
)


class Credentials(NamedTuple):
    api_key: str

    def __repr__(self) -> str:
        return "Creds(api_key=[masked])"
