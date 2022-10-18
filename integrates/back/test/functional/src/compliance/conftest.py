# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
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
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("compliance")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    agent_token=(
                        "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJjaXBABCXYZ"
                    ),
                    context="This is a dummy context",
                    created_by="unknown",
                    created_date="2020-05-20T22:00:00+00:00",
                    description="this is group1",
                    language=GroupLanguage.EN,
                    name="group1",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date="2020-05-20T22:00:00+00:00",
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                        service=GroupService.WHITE,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    tags={"testing"},
                    business_id="1867",
                    business_name="Testing Company",
                    sprint_duration=3,
                    sprint_start_date="2022-06-06T00:00:00",
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
                ),
            },
        ],
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
    }

    return await db.populate({**generic_data["db_data"], **data})
