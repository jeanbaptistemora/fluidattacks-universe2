# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    ComplianceUnreliableIndicators,
)
from .utils import (
    format_unreliable_indicators_item,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def update_unreliable_indicators(
    *,
    indicators: ComplianceUnreliableIndicators,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["compliance_unreliable_indicators"],
        values={},
    )
    unreliable_indicators = format_unreliable_indicators_item(indicators)
    await operations.update_item(
        item=unreliable_indicators,
        key=primary_key,
        table=TABLE,
    )
