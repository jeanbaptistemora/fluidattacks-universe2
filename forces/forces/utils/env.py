# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import os
from typing import (
    Literal,
)

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_ENDPOINT = "https://127.0.0.1:8001/api"
PROD_ENDPOINT = "https://app.fluidattacks.com/api"
ENDPOINT: str = os.environ.get("API_ENDPOINT", PROD_ENDPOINT)


def guess_environment() -> Literal["development", "production"]:
    return "development" if ENDPOINT != PROD_ENDPOINT else "production"
