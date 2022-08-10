# pylint: disable=import-error
from back.test import (
    db,
)
from collections import (
    defaultdict,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingStatus,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
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
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRoot,
    GitRootCloning,
    GitRootState,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityVerification,
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("upload_file")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    description="-",
                    language=GroupLanguage.EN,
                    name="group123",
                    state=GroupState(
                        has_machine=False,
                        has_squad=False,
                        managed=GroupManaged["MANAGED"],
                        modified_by="admin@gmail.com",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    sprint_start_date="2022-06-06T00:00:00",
                ),
            },
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
            {
                "finding": Finding(
                    id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection - C Sharp SQL API",
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email="test1@gmail.com",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.2"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("0.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_integrity_impact=Decimal("0"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_severity_scope=Decimal("0"),
                        modified_privileges_required=Decimal("0.27"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        privileges_required=Decimal("0.62"),
                        severity_scope=Decimal("1.2"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        user_interaction=Decimal("0.85"),
                    ),
                    requirements=(
                        "REQ.0132. Passwords (phrase type) "
                        "must be at least 3 words long."
                    ),
                    threat="Updated threat",
                    attack_vector_description=(
                        "This is an updated attack vector"
                    ),
                    evidences=FindingEvidences(
                        evidence1=FindingEvidence(
                            description="evidence1",
                            url=(
                                "group1-3c475384-834c-47b0-"
                                "ac71-a41a022e401c-evidence1"
                            ),
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        records=FindingEvidence(
                            description="records",
                            url=(
                                "group1-3c475384-834c-47b0-"
                                "ac71-a41a022e401c-records"
                            ),
                            modified_date="2111-11-19T13:37:10+00:00",
                        ),
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:00:01+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:00:02+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:00:03+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2018-04-08T00:00:04+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                    ),
                ],
                "historic_verification": [
                    FindingVerification(
                        comment_id="42343434",
                        modified_by="requester@gmail.com",
                        modified_date="2018-04-08T01:45:11+00:00",
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
                            "be09edb7-cd5c-47ed-bee4-97c645acdcea",
                        },
                    ),
                    FindingVerification(
                        comment_id="54545454",
                        modified_by="reattacker@fluidattack.com",
                        modified_date="2018-04-08T01:45:12+00:00",
                        status=FindingVerificationStatus.VERIFIED,
                        vulnerability_ids={
                            "be09edb7-cd5c-47ed-bee4-97c645acdcea",
                        },
                    ),
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=1,
                    unreliable_open_vulnerabilities=2,
                    unreliable_newest_vulnerability_report_date=(
                        "2018-04-08T00:43:11+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        "2018-04-08T00:43:11+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        "2018-04-08T00:43:11+00:00"
                    ),
                    unreliable_status=FindingStatus.OPEN,
                    unreliable_where=(
                        "192.168.1.44, 192.168.1.45, 192.168.1.46"
                    ),
                ),
            },
        ],
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date="2020-11-19T13:37:10+00:00",
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    group_name="group1",
                    id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        environment_urls=["https://.com"],
                        git_environment_urls=[
                            GitEnvironmentUrl(
                                url="https://test.com",
                                id="78dd64d3198473115a7f5263d27bed15f9f2fc07",
                            )
                        ],
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date="2020-11-19T13:37:10+00:00",
                        nickname="universe",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date="2020-11-19T13:37:10+00:00",
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    group_name="group1",
                    id="e782e588-060d-4ae7-8930-3c11d2ba4395",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        environment_urls=["https://.com"],
                        git_environment_urls=[
                            GitEnvironmentUrl(
                                url="https://testtest.com",
                                id="683d198c-f88d-4a92-a02d-7377ad2dca45",
                            )
                        ],
                        gitignore=["node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date="2020-11-19T13:37:10+00:00",
                        nickname="universe123",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
        "toe_inputs": (
            ToeInput(
                attacked_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                attacked_by="",
                be_present=True,
                be_present_until=None,
                component="https://example.com",
                entry_point="phone",
                first_attack_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                seen_at=None,
                seen_first_time_by="",
                unreliable_root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
            ),
            ToeInput(
                attacked_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                attacked_by="",
                be_present=True,
                be_present_until=None,
                component="https://test_new_closed.com",
                entry_point="phone",
                first_attack_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                seen_at=None,
                seen_first_time_by="",
                unreliable_root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
            ),
        ),
        "toe_lines": (
            ToeLines(
                attacked_at=None,
                attacked_by="test@test.com",
                attacked_lines=23,
                be_present=True,
                be_present_until=None,
                comments="",
                filename="path/to/file1.ext",
                first_attack_at=None,
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer1@gmail.com",
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                loc=4324,
                modified_date=datetime.fromisoformat(
                    "2020-11-16T15:41:04+00:00"
                ),
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                seen_at=datetime.fromisoformat("2020-01-01T15:41:04+00:00"),
                sorts_risk_level=0,
            ),
            ToeLines(
                attacked_at=datetime.fromisoformat(
                    "2021-02-20T05:00:00+00:00"
                ),
                attacked_by="test2@test.com",
                attacked_lines=4,
                be_present=True,
                be_present_until=None,
                comments="comment 2",
                filename="test/1",
                first_attack_at=datetime.fromisoformat(
                    "2020-02-19T15:41:04+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer2@gmail.com",
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                loc=180,
                modified_date=datetime.fromisoformat(
                    "2020-11-15T15:41:04+00:00"
                ),
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                seen_at=datetime.fromisoformat("2020-02-01T15:41:04+00:00"),
                sorts_risk_level=-1,
            ),
        ),
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    specific="4444",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T00:43:11+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:43:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_last_reattack_requester=(
                            "requester@gmail.com"
                        ),
                        unreliable_last_requested_reattack_date=(
                            "2018-04-08T01:45:11+00:00"
                        ),
                        unreliable_report_date="2018-04-08T00:43:11+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date="2018-04-08T01:45:11+00:00",
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    where="192.168.1.44",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce9",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    specific="4545",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T00:44:11+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:44:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_last_reattack_requester=(
                            "requester@gmail.com"
                        ),
                        unreliable_last_requested_reattack_date=(
                            "2018-04-08T01:45:11+00:00"
                        ),
                        unreliable_report_date="2018-04-08T00:44:11+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date="2018-04-08T01:45:11+00:00",
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    where="192.168.1.45",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdcea",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    specific="4646",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.CLOSED,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=(
                            "2018-04-08T01:45:12+00:00"
                        ),
                        unreliable_last_reattack_requester=(
                            "requester@gmail.com"
                        ),
                        unreliable_last_requested_reattack_date=(
                            "2018-04-08T01:45:11+00:00"
                        ),
                        unreliable_report_date="2018-04-08T00:45:11+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date="2018-04-08T01:45:12+00:00",
                        status=VulnerabilityVerificationStatus.VERIFIED,
                    ),
                    where="192.168.1.46",
                ),
                "historic_state": [
                    VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T01:45:12+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.CLOSED,
                    ),
                ],
                "historic_verification": [
                    VulnerabilityVerification(
                        modified_date="2018-04-08T01:45:11+00:00",
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    VulnerabilityVerification(
                        modified_date="2018-04-08T01:45:12+00:00",
                        status=VulnerabilityVerificationStatus.VERIFIED,
                    ),
                ],
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdceb",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    specific="4747",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T00:44:11+00:00",
                        source=Source.MACHINE,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:44:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_last_reattack_requester=(
                            "requester@gmail.com"
                        ),
                        unreliable_last_requested_reattack_date=(
                            "2018-04-08T01:45:11+00:00"
                        ),
                        unreliable_report_date="2018-04-08T00:44:11+00:00",
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    where="192.168.1.47",
                ),
            },
        ],
        "policies": [
            {
                "level": "group",
                "subject": generic_data["global_vars"]["admin_email"],
                "object": "group123",
                "role": "admin",
            },
        ],
    }
    merge_dict = defaultdict(list)
    for dict_data in (generic_data["db_data"], data):
        for key, value in dict_data.items():
            merge_dict[key].extend(value)

    return await db.populate(merge_dict)
