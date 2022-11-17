# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.types import (
    Policies,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_organization")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "groups": [],
        "organizations": [
            {
                "organization": Organization(
                    created_by="johndoe@fluidattacks.com",
                    created_date="2022-10-21T15:58:31.280182",
                    country="Colombia",
                    id="967e17db-6345-4504-a5c4-285e5f8068c6",
                    name="trialorg",
                    policies=Policies(
                        modified_by="johndoe@fluidattacks.com",
                        modified_date="2022-10-21T15:58:31.280182",
                    ),
                    state=OrganizationState(
                        modified_by="johndoe@fluidattacks.com",
                        modified_date="2022-10-21T15:58:31.280182",
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ],
        "policies": [
            *generic_data["db_data"]["policies"],
            {
                "level": "organization",
                "subject": "johndoe@fluidattacks.com",
                "object": "ORG#967e17db-6345-4504-a5c4-285e5f8068c6",
                "role": "user_manager",
            },
        ],
        "stakeholders": [
            *generic_data["db_data"]["stakeholders"],
            Stakeholder(
                email="johndoe@fluidattacks.com",
                first_name="John",
                is_registered=True,
                last_name="Doe",
                role="user_manager",
            ),
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
