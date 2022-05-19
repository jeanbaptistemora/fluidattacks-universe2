# flake8: noqa
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
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
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
        "orgs": [
            {
                "name": "org123",
                "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                "users": ("test@fluidattacks.com",),
                "groups": ("group123",),
                "policy": {},
            },
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
                        managed=True,
                        modified_by="test@fluidattacks.com",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                ),
            },
        ],
        "roots": [
            GitRoot(
                cloning=GitRootCloning(
                    modified_date="2022-02-10T14:58:10+00:00",
                    reason="Cloned successfully",
                    status=GitCloningStatus.OK,
                ),
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
                    modified_date="2022-02-10T14:58:10+00:00",
                    nickname="test",
                    other="",
                    reason="",
                    status=RootStatus.ACTIVE,
                    url="https://gitlab.com/fluidattacks/test",
                ),
                type=RootType.GIT,
            ),
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
                    "source_nickname": "test",
                    "target_nickname": "test123",
                }
            ),
            batch_job_id=None,
            queue="unlimited_spot",
            key="1",
        ),
    )

    await db.populate_actions(actions)
    return await db.populate(data)
