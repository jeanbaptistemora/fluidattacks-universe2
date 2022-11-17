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
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
    GroupUnreliableIndicators,
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
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization_vulnerabilities")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    created_by="user_manager@domain.com",
                    created_date="2022-09-12T19:00:00-05:00",
                    description="Test group",
                    language=GroupLanguage.EN,
                    name="test_group_1",
                    organization_id="c4fc4bde-93fa-44d1-981b-9ce16c5435e8",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged.MANAGED,
                        modified_by="user_manager@fomain.com",
                        modified_date="2022-09-12T19:10:00-05:00",
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
                "unreliable_indicators": GroupUnreliableIndicators(
                    closed_vulnerabilities=10,
                    max_severity=Decimal("8.0"),
                ),
            }
        ],
        "organizations": [
            {
                "organization": Organization(
                    created_by="user_manager@domain.com",
                    created_date="2022-09-12T18:00:00-05:00",
                    country="Colombia",
                    id="c4fc4bde-93fa-44d1-981b-9ce16c5435e8",
                    name="test_organization_1",
                    policies=Policies(
                        max_acceptance_days=15,
                        modified_by="user_manager@domain.com",
                        modified_date="2022-09-12T18:10:00-05:00",
                    ),
                    state=OrganizationState(
                        status=OrganizationStateStatus.ACTIVE,
                        modified_by="user_manager@domain.com",
                        modified_date="2022-09-12T18:00:00-05:00",
                    ),
                )
            }
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
