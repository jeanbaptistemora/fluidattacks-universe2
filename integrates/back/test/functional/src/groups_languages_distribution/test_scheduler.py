# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    get_new_context,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
)
from decimal import (
    Decimal,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("groups_languages_distribution")
async def test_update_groups_languages(populate: bool) -> None:
    assert populate

    loaders = get_new_context()
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load("group1")
    )
    assert group_indicators.closed_vulnerabilities == 10
    assert group_indicators.code_languages is None
    assert group_indicators.max_severity == Decimal("8.0")
