# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingState,
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
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    URLRoot,
    URLRootState,
)
from db_model.types import (
    Policies,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityUnreliableIndicators,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_url_root")
@pytest.fixture(autouse=True, scope="session")
async def populate() -> bool:
    data: dict[str, Any] = {
        "policies": [
            {
                "level": "user",
                "subject": "test@fluidattacks.com",
                "object": "self",
                "role": "admin",
            },
        ],
        "organizations": [
            {
                "organization": Organization(
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="org123",
                    policies=Policies(
                        modified_by="test@fluidattacks.com",
                        max_acceptance_days=7,
                        modified_date="2019-11-22T20:07:57+00:00",
                    ),
                    state=OrganizationState(
                        modified_by="test@fluidattacks.com",
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
                    name="group123",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="test@fluidattacks.com",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.BLACK,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    sprint_start_date="2022-06-06T00:00:00",
                ),
            },
        ],
        "roots": [
            {
                "root": URLRoot(
                    group_name="group123",
                    id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    organization_name="org123",
                    state=URLRootState(
                        host="app.fluidattacks.com",
                        modified_by="test@fluidattacks.com",
                        modified_date="2022-02-10T14:58:10+00:00",
                        nickname="test_nickname_3",
                        other=None,
                        path="/",
                        port="8080",
                        protocol="HTTPS",
                        reason=None,
                        status=RootStatus.ACTIVE,
                    ),
                    type=RootType.URL,
                ),
                "historic_state": [],
            }
        ],
        "findings": [
            {
                "finding": Finding(
                    id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
                    group_name="group123",
                    state=FindingState(
                        modified_by="test@fluidattacks.com",
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection",
                    hacker_email="test@fluidattacks.com",
                ),
                "historic_state": [],
                "historic_verification": [],
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    finding_id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
                    group_name="group123",
                    hacker_email="test@fluidattacks.com",
                    id="64bf8e56-0b3c-432a-bff7-c3eef56c47b7",
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    specific="999",
                    state=VulnerabilityState(
                        modified_by="test@fluidattacks.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2018-04-08T00:45:11+00:00",
                        unreliable_source=Source.ASM,
                    ),
                    where="test/data/lib_path/f060/csharp.cs",
                    commit="4af88aa99f5ba20456560dd89ed380cbf81c2b1e",
                ),
            },
        ],
    }

    return await db.populate(data)
