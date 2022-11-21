# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    get_new_context,
)
from organizations.domain import (
    get_group_names,
)
import pytest
from schedulers.organization_vulnerabilities import (
    get_data,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization_vulnerabilities")
async def test_organization_vulnerabilities_rows(populate: bool) -> None:
    assert populate

    loaders = get_new_context()
    org_id = "ORG#c4fc4bde-93fa-44d1-981b-9ce16c5435e8"
    org_name = "test_organization_1"
    all_groups_names = await get_group_names(loaders, org_id)

    rows: list[list[str]] = await get_data(
        groups=tuple(all_groups_names),
        loaders=loaders,
        organization_name=org_name,
    )

    assert len(rows[0]) == 52
    assert rows[0][-1] == "Group"
