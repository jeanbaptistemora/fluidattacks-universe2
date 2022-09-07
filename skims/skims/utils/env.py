# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from os import (
    environ,
)
from typing import (
    Literal,
    Union,
)


def guess_environment() -> Union[
    Literal["development"],
    Literal["production"],
]:
    return (
        "production"
        if environ.get("CI_COMMIT_REF_NAME", "trunk") == "trunk"
        else "development"
    )
