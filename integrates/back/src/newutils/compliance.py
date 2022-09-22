# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


import aiofiles
from context import (
    FI_INTEGRATES_CRITERIA_COMPLIANCE,
)
from typing import (
    Any,
)
import yaml


async def get_compliance_file() -> dict[str, Any]:
    """Parses the compliance info yaml from the repo into a dictionary."""
    async with aiofiles.open(
        FI_INTEGRATES_CRITERIA_COMPLIANCE, encoding="utf-8"
    ) as handler:
        return yaml.safe_load(await handler.read())
