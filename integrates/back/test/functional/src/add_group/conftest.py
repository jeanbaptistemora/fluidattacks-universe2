# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.types import (
    Policies,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "organizations": [
            {
                "organization": Organization(
                    country="Colombia",
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="orgtest",
                    policies=Policies(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date="2019-11-22T20:07:57+00:00",
                    ),
                    state=OrganizationState(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date="2019-11-22T20:07:57+00:00",
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ],
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date="2020-05-20T22:00:00+00:00",
                    description="-",
                    language=GroupLanguage.EN,
                    name="group2",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.BLACK,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.ONESHOT,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    sprint_start_date="2022-06-06T00:00:00",
                ),
            },
            {
                "group": Group(
                    created_by="unknown",
                    created_date="2020-05-20T22:00:00+00:00",
                    description="-",
                    language=GroupLanguage.EN,
                    name="group3",
                    state=GroupState(
                        has_machine=False,
                        has_squad=False,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.BLACK,
                        status=GroupStateStatus.DELETED,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.ONESHOT,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    sprint_start_date="2022-06-06T00:00:00",
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
