# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
)
from batch.enums import (
    Action,
)
from db_model.enums import (
    GitCloningStatus,
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
    GitRoot,
    GitRootCloning,
    GitRootState,
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
import json
from newutils.datetime import (
    get_as_epoch,
    get_now,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("move_root")
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
                        service=GroupService.WHITE,
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
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date="2022-02-10T14:58:10+00:00",
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by="admin@gmail.com",
                    created_date="2022-02-09T14:58:10+00:00",
                    group_name="group123",
                    id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    organization_name="org123",
                    state=GitRootState(
                        branch="master",
                        environment_urls=[],
                        environment="production",
                        git_environment_urls=[],
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="test@fluidattacks.com",
                        modified_date="2022-02-09T14:58:10+00:00",
                        nickname="test",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/test",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": (
                    GitRootState(
                        branch="master",
                        environment_urls=[],
                        environment="production",
                        git_environment_urls=[],
                        gitignore=["node_modules/*"],
                        includes_health_check=False,
                        modified_by="test@fluidattacks.com",
                        modified_date="2022-02-10T14:58:10+00:00",
                        nickname="test123",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/test",
                    ),
                ),
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
                    created_by="test@fluidattacks.com",
                    created_date="2018-04-08T00:45:11+00:00",
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
            {
                "vulnerability": Vulnerability(
                    created_by="test@fluidattacks.com",
                    created_date="2018-04-08T00:45:11+00:00",
                    finding_id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
                    group_name="group123",
                    hacker_email="test@fluidattacks.com",
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
                    created_by="test@fluidattacks.com",
                    created_date="2018-04-08T00:45:14+00:00",
                    finding_id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
                    group_name="group123",
                    hacker_email="test@fluidattacks.com",
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
    actions: tuple[dict[str, Any], ...] = (
        dict(
            action_name=Action.UPDATE_NICKNAME.value,
            entity="88637616-41d4-4242-854a-db8ff7fe1ab6",
            subject="test@fluidattacks.com",
            time=str(get_as_epoch(get_now())),
            additional_info=json.dumps(
                {
                    "group_name": "group123",
                    "nickname": "test123",
                    "old_nickname": "test",
                }
            ),
            batch_job_id=None,
            queue="small",
            key="1",
        ),
    )

    await db.populate_actions(actions)
    return await db.populate(data)
