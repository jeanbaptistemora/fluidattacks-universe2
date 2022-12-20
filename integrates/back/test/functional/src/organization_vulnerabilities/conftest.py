# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
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
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization_vulnerabilities")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    created_by="user_manager@domain.com",
                    created_date=datetime.fromisoformat(
                        "2022-09-13T00:00:00+00:00"
                    ),
                    description="Test group",
                    language=GroupLanguage.EN,
                    name="test_group_1",
                    organization_id="c4fc4bde-93fa-44d1-981b-9ce16c5435e8",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged.MANAGED,
                        modified_by="user_manager@fomain.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-13T00:00:00+00:00"
                        ),
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
                    created_date=datetime.fromisoformat(
                        "2022-09-12T23:00:00+00:00"
                    ),
                    country="Colombia",
                    id="c4fc4bde-93fa-44d1-981b-9ce16c5435e8",
                    name="test_organization_1",
                    policies=Policies(
                        max_acceptance_days=15,
                        modified_by="user_manager@domain.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-12T23:00:00+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        status=OrganizationStateStatus.ACTIVE,
                        modified_by="user_manager@domain.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-12T23:00:00+00:00"
                        ),
                    ),
                )
            }
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
