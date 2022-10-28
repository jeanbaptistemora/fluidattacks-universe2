# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.enrollment.types import (
    Enrollment,
    Trial,
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
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.types import (
    Policies,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_enrollment")
@pytest.fixture(autouse=True, scope="session")
async def populate() -> bool:
    data = {
        "enrollments": [
            Enrollment(
                email="janedoe@fluidattacks.com",
                enrolled=True,
                trial=Trial(
                    completed=False,
                    extension_date="",
                    extension_days=0,
                    start_date="2022-10-21T15:58:31.280182",
                ),
            ),
        ],
        "groups": [
            {
                "group": Group(
                    created_by="johndoe@fluidattacks.com",
                    created_date="2022-10-21T15:58:31.280182",
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup",
                    organization_id="e314a87c-223f-44bc-8317-75900f2ffbc7",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="johndoe@fluidattacks.com",
                        modified_date="2022-10-21T15:58:31.280182",
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
            },
        ],
        "organizations": [
            {
                "organization": Organization(
                    country="Colombia",
                    id="e314a87c-223f-44bc-8317-75900f2ffbc7",
                    name="testorg",
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
            {
                "level": "organization",
                "subject": "johndoe@fluidattacks.com",
                "object": "testorg",
                "role": "user_manager",
            },
            {
                "level": "group",
                "subject": "johndoe@fluidattacks.com",
                "object": "testgroup",
                "role": "user_manager",
            },
        ],
        "stakeholders": [
            Stakeholder(
                email="johndoe@fluidattacks.com",
                first_name="John",
                is_registered=True,
                last_name="Doe",
            ),
            Stakeholder(
                email="janedoe@fluidattacks.com",
                first_name="Jane",
                is_registered=True,
                last_name="Doe",
            ),
        ],
    }
    return await db.populate(data)
