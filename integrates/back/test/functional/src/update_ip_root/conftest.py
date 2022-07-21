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
from db_model.organization_access.types import (
    OrganizationAccess,
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
    IPRoot,
    IPRootState,
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
@pytest.mark.resolver_test_group("update_ip_root")
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
        "organization_access": [
            OrganizationAccess(
                organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                email="test@fluidattacks.com",
            ),
        ],
        "groups": [
            {
                "group": Group(
                    description="-",
                    language=GroupLanguage.EN,
                    name="group123",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANUALLY"],
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
                "root": IPRoot(
                    group_name="group123",
                    id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    organization_name="org123",
                    state=IPRootState(
                        address="https://gitlab.com/fluidattacks/test",
                        modified_by="test@fluidattacks.com",
                        modified_date="2022-02-10T14:58:10+00:00",
                        nickname="test123",
                        other="",
                        port="444",
                        reason="",
                        status=RootStatus.ACTIVE,
                    ),
                    type=RootType.IP,
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
            {
                "vulnerability": Vulnerability(
                    finding_id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
                    id="06b0e56b-db07-4420-88f7-f8ad1561a444",
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    specific="909",
                    state=VulnerabilityState(
                        modified_by="test@fluidattacks.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2019-04-08T00:45:11+00:00",
                        unreliable_source=Source.ASM,
                    ),
                    where="test/data/lib_path/f050/csharp.cs",
                    commit="f58490fab40762048474be2bae4735c82714946e",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce9",
                    specific="9999",
                    state=VulnerabilityState(
                        modified_by="test@fluidattacks.com",
                        modified_date="2018-04-08T00:45:14+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2018-04-08T00:45:14+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    type=VulnerabilityType.PORTS,
                    where="192.168.1.20",
                )
            },
        ],
    }

    return await db.populate(data)
