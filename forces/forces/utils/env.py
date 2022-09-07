# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import os
from os import (
    environ,
)
from typing import (
    Literal,
    Union,
)

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def guess_environment() -> Union[
    Literal["development"],
    Literal["production"],
]:
    if any(
        (
            "universe/" in BASE_DIR,
            environ.get("CI_COMMIT_REF_NAME", "trunk") != "trunk",
        )
    ):
        return "development"

    return "production"  # pragma: no cover
