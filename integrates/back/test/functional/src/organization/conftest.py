# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationPolicies,
    OrganizationState,
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
        "organizations": [
            {
                "organization": Organization(
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="orgtest",
                    policies=OrganizationPolicies(
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
                    policies=OrganizationPolicies(
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
                    "executive@gmail.com",
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
        "organization_groups": [
            {
                "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                "groups": [
                    "group1",
                ],
            },
            {
                "id": "8a7c8089-92df-49ec-8c8b-ee83e4ff3256",
                "groups": [
                    "group2",
                ],
            },
        ],
        "orgs": [],
    }
    return await db.populate({**generic_data["db_data"], **data})
