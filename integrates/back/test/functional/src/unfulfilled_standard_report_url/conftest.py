# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.compliance.types import (
    ComplianceStandard,
    ComplianceUnreliableIndicators,
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
    GroupUnreliableIndicators,
    UnfulfilledStandard,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationStandardCompliance,
    OrganizationState,
    OrganizationUnreliableIndicators,
)
from db_model.types import (
    Policies,
)
from decimal import (
    Decimal,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("unfulfilled_standard_report_url")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "compliances": [
            {
                "compliance": {
                    "unreliable_indicators": ComplianceUnreliableIndicators(
                        standards=[
                            ComplianceStandard(
                                avg_organization_compliance_level=Decimal(
                                    "0.5"
                                ),
                                best_organization_compliance_level=Decimal(
                                    "0.5"
                                ),
                                standard_name="bsimm",
                                worst_organization_compliance_level=Decimal(
                                    "0.5"
                                ),
                            ),
                        ]
                    )
                }
            }
        ],
        "groups": [
            {
                "group": Group(
                    agent_token=(
                        "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJjaXBABCXYZ"
                    ),
                    context="This is a dummy context",
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="this is group1",
                    language=GroupLanguage.EN,
                    name="group1",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        status=GroupStateStatus.ACTIVE,
                        tags={"testing"},
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                        service=GroupService.WHITE,
                    ),
                    organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    business_id="1867",
                    business_name="Testing Company",
                    sprint_duration=3,
                    sprint_start_date=datetime.fromisoformat(
                        "2022-06-06T00:00:00+00:00"
                    ),
                ),
                "unreliable_indicators": GroupUnreliableIndicators(
                    closed_vulnerabilities=1,
                    open_vulnerabilities=2,
                    last_closed_vulnerability_days=40,
                    last_closed_vulnerability_finding="475041521",
                    max_open_severity=Decimal("4.3"),
                    max_open_severity_finding="475041521",
                    open_findings=2,
                    mean_remediate=Decimal("2.0"),
                    mean_remediate_low_severity=Decimal("3.0"),
                    mean_remediate_medium_severity=Decimal("4.0"),
                    unfulfilled_standards=[
                        UnfulfilledStandard(
                            name="bsimm",
                            unfulfilled_requirements=["155", "159", "273"],
                        )
                    ],
                ),
            },
        ],
        "organizations": [
            {
                "organization": Organization(
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="orgtest",
                    policies=Policies(
                        modified_by="admin@gmail.com",
                        max_acceptance_days=7,
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        vulnerability_grace_period=5,
                    ),
                    state=OrganizationState(
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
                "unreliable_indicators": OrganizationUnreliableIndicators(
                    compliance_level=Decimal("0.8"),
                    compliance_weekly_trend=Decimal("0.02"),
                    estimated_days_to_full_compliance=Decimal("3"),
                    standard_compliances=[
                        OrganizationStandardCompliance(
                            standard_name="bsimm",
                            compliance_level=Decimal("0.3"),
                        )
                    ],
                ),
            },
        ],
    }

    return await db.populate({**generic_data["db_data"], **data})
