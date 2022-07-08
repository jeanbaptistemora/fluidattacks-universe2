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
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    description="-",
                    language=GroupLanguage.EN,
                    name="group1",
                    state=GroupState(
                        has_machine=False,
                        has_squad=True,
                        managed=GroupManaged["MANUALLY"],
                        modified_by="unknown",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                ),
            },
            {
                "group": Group(
                    description="-",
                    language=GroupLanguage.EN,
                    name="group2",
                    state=GroupState(
                        has_machine=False,
                        has_squad=True,
                        managed=GroupManaged["MANUALLY"],
                        modified_by="unknown",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.BLACK,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.ONESHOT,
                    ),
                    organization_id="8a7c8089-92df-49ec-8c8b-ee83e4ff3256",
                ),
            },
        ],
        "organizations": [
            {
                "organization": Organization(
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="orgtest",
                    policies=Policies(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date="2019-11-22T20:07:57+00:00",
                        max_acceptance_days=90,
                        max_number_acceptances=4,
                        max_acceptance_severity=Decimal("7.0"),
                        min_acceptance_severity=Decimal("3.0"),
                        min_breaking_severity=Decimal("2.0"),
                        vulnerability_grace_period=5,
                    ),
                    state=OrganizationState(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date="2019-11-22T20:07:57+00:00",
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    id="8a7c8089-92df-49ec-8c8b-ee83e4ff3256",
                    name="acme",
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
        "organization_users": [
            {
                "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                "users": [
                    "admin@gmail.com",
                    "hacker@gmail.com",
                    "reattacker@gmail.com",
                    "user@gmail.com",
                    "user_manager@gmail.com",
                    "vulnerability_manager@gmail.com",
                    "customer_manager@fluidattacks.com",
                    "resourcer@gmail.com",
                    "reviewer@gmail.com",
                ],
            },
            {
                "id": "8a7c8089-92df-49ec-8c8b-ee83e4ff3256",
                "users": [
                    "admin@gmail.com",
                ],
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
