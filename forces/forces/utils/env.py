# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import os
from typing import (
    Literal,
)

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def guess_environment() -> Literal["development"] | Literal["production"]:
    if any(
        (
            "universe/" in BASE_DIR,
            (
                os.environ.get("CI_COMMIT_REF_NAME", "trunk") != "trunk"
                and os.environ.get("CI_PROJECT_NAMESPACE") == "fluidattacks"
            ),
        )
    ):
        return "development"

    return "production"  # pragma: no cover
