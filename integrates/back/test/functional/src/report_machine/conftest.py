# flake8: noqa
from back.test import (
    db,
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
from db_model.findings.types import (  # type: ignore
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
    GitRoot,
    GitRootCloning,
    GitRootState,
    RootEnvironmentUrl,
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
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("report_machine")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="This is a dummy description",
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
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    business_id="123",
                    business_name="acme",
                    sprint_duration=3,
                ),
            }
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
                    created_date="2022-02-10T14:58:10+00:00",
                    group_name="group1",
                    id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment_urls=[],
                        environment="production",
                        git_environment_urls=[
                            RootEnvironmentUrl(
                                url="http://localhost:48000/",
                                id="3aca06ef047ca0195f8ffc7ea5b64605b3f779cb",
                                secrets=[],
                            )
                        ],
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date="2022-02-10T14:58:10+00:00",
                        nickname="nickname",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date="2022-02-10T14:58:10+00:00",
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by="admin@gmail.com",
                    created_date="2022-02-10T14:58:10+00:00",
                    group_name="group1",
                    id="9059f0cb-3b55-404b-8fc5-627171f424ad",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment_urls=[],
                        environment="production",
                        git_environment_urls=[],
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date="2022-02-10T14:58:10+00:00",
                        nickname="nickname2",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname2",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
        "findings": [
            {
                "finding": Finding(
                    id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:11+00:00"
                        ),
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
                        evidence5=FindingEvidence(
                            description="evidence5",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence5",
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        records=FindingEvidence(
                            description="records",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-records",
                            modified_date=datetime.fromisoformat(
                                "2111-11-19T13:37:10+00:00"
                            ),
                        ),
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:12+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:13+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:14+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                    ),
                ],
                "historic_verification": [
                    FindingVerification(
                        comment_id="42343434",
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-01T00:45:12+00:00"
                        ),
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "6dbc13e1-5cfc-3b44-9b70-bb7566c641sz",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date=(
                        "2020-12-26T05:45:00+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        "2020-02-24T05:45:00+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        "2018-04-01T05:45:00+00:00"
                    ),
                    unreliable_status=FindingStatus.OPEN,
                    unreliable_where="192.168.1.2",
                ),
            },
            {
                "finding": Finding(
                    id="4629a805-7ce5-4cd1-a39a-4579ec6fd985",
                    group_name="group1",
                    state=FindingState(
                        modified_by="hacker@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-19T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="117. Unverifiable files",
                    recommendation="Recommendation",
                    description="Description",
                    hacker_email="hacker@fluidattacks.com",
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
                    requirements="Requirement",
                    threat="Threat",
                    attack_vector_description="Attack vector",
                    evidences=FindingEvidences(
                        evidence5=FindingEvidence(
                            description="evidence5",
                            url="group1-4629a805-7ce5-4cd1-a39a-4579ec6fd985-evidence5",
                            modified_date=datetime.fromisoformat(
                                "2022-10-19T05:00:05+00:00"
                            ),
                        ),
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="hacker@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-19T05:00:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="hacker@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-19T05:00:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                ],
                "historic_verification": [],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=0,
                    unreliable_open_vulnerabilities=1,
                    unreliable_newest_vulnerability_report_date=(
                        "2022-10-19T05:00:15+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        "2022-10-19T05:00:15+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        "2022-10-19T05:00:15+00:00"
                    ),
                    unreliable_status=FindingStatus.OPEN,
                    unreliable_where=".project",
                ),
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date="2018-04-08T00:45:15+00:00",
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="4dbc03e0-4cfc-4b33-9b70-bb7566c460bd",
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date="2018-04-08T00:45:15+00:00",
                        source=Source.MACHINE,
                        specific="52",
                        status=VulnerabilityStateStatus.OPEN,
                        where="back/src/model/user/index.js",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date="2018-04-08T00:45:15+00:00",
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="4dbc01e0-4cfc-4b77-9b71-bb7566c60bg",
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date="2018-04-08T00:45:15+00:00",
                        source=Source.MACHINE,
                        specific="12",
                        status=VulnerabilityStateStatus.OPEN,
                        where="back/src/controller/user/index.js",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date="2018-04-08T00:45:15+00:00",
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="5dbc02e0-4cfc-4b33-9b70-bb7566c230cv",
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date="2018-04-08T00:45:15+00:00",
                        source=Source.MACHINE,
                        specific="64",
                        status=VulnerabilityStateStatus.OPEN,
                        where="front/index.html",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date="2018-04-08T00:45:15+00:00",
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="6dbc13e1-5cfc-3b44-9b70-bb7566c641sz",
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date="2018-04-08T00:45:15+00:00",
                        source=Source.MACHINE,
                        specific="35",
                        status=VulnerabilityStateStatus.OPEN,
                        where="back/src/index.js",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@fluidattacks.com",
                    created_date="2022-10-19T05:00:20+00:00",
                    finding_id="4629a805-7ce5-4cd1-a39a-4579ec6fd985",
                    group_name="group1",
                    hacker_email="hacker@fluidattacks.com",
                    id="dadb5c43-90ab-47ea-a80f-db89a940cd54",
                    state=VulnerabilityState(
                        modified_by="hacker@fluidattacks.com",
                        modified_date="2022-10-19T05:00:20+00:00",
                        source=Source.ASM,
                        specific="0",
                        status=VulnerabilityStateStatus.OPEN,
                        where=".project",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2022-10-19T05:00:20+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
        ],
        "toe_lines": (
            ToeLines(
                attacked_at=None,
                attacked_by="machine@fluidattacks.com",
                attacked_lines=23,
                be_present=True,
                be_present_until=None,
                comments="",
                filename="nickname/back/src/model/user/index.js",
                first_attack_at=None,
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer1@gmail.com",
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                loc=4324,
                modified_date=datetime.fromisoformat(
                    "2020-11-16T15:41:04+00:00"
                ),
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                seen_at=datetime.fromisoformat("2020-01-01T15:41:04+00:00"),
                sorts_risk_level=0,
            ),
            ToeLines(
                attacked_at=datetime.fromisoformat(
                    "2021-02-20T05:00:00+00:00"
                ),
                attacked_by="machine@fluidattacks.com",
                attacked_lines=4,
                be_present=True,
                be_present_until=None,
                comments="comment 2",
                filename="back/src/index.js",
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
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                seen_at=datetime.fromisoformat("2020-02-01T15:41:04+00:00"),
                sorts_risk_level=-1,
            ),
            ToeLines(
                attacked_at=datetime.fromisoformat(
                    "2021-02-20T05:00:00+00:00"
                ),
                attacked_by="machine@fluidattacks.com",
                attacked_lines=4,
                be_present=True,
                be_present_until=None,
                comments="comment 2",
                filename="skims/test/data/lib_path/f011/requirements.txt",
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
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                seen_at=datetime.fromisoformat("2020-02-01T15:41:04+00:00"),
                sorts_risk_level=-1,
            ),
            ToeLines(
                attacked_at=datetime.fromisoformat(
                    "2020-01-14T15:41:04+00:00"
                ),
                attacked_by="machine@fluidattacks.com",
                attacked_lines=120,
                be_present=True,
                be_present_until=None,
                comments="",
                filename="front/index.html",
                first_attack_at=datetime.fromisoformat(
                    "2020-01-14T15:41:04+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer3@gmail.com",
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c3",
                loc=243,
                modified_date=datetime.fromisoformat(
                    "2020-11-16T15:41:04+00:00"
                ),
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                seen_at=datetime.fromisoformat("2019-01-01T15:41:04+00:00"),
                sorts_risk_level=80,
            ),
            ToeLines(
                attacked_at=datetime.fromisoformat(
                    "2021-02-20T05:00:00+00:00"
                ),
                attacked_by="machine@fluidattacks.com",
                attacked_lines=1,
                be_present=True,
                be_present_until=None,
                comments="",
                filename="skims/test/data/lib_path/f011/build.gradle",
                first_attack_at=datetime.fromisoformat(
                    "2020-02-19T15:41:04+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer2@gmail.com",
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c5",
                loc=180,
                modified_date=datetime.fromisoformat(
                    "2020-11-15T15:41:04+00:00"
                ),
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                seen_at=datetime.fromisoformat("2020-02-01T15:41:04+00:00"),
                sorts_risk_level=-1,
            ),
            ToeLines(
                attacked_at=datetime.fromisoformat(
                    "2021-02-20T05:00:00+00:00"
                ),
                attacked_by="machine@fluidattacks.com",
                attacked_lines=1,
                be_present=True,
                be_present_until=None,
                comments="",
                filename="MyJar.jar",
                first_attack_at=datetime.fromisoformat(
                    "2020-02-19T15:41:04+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer2@gmail.com",
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c5",
                loc=180,
                modified_date=datetime.fromisoformat(
                    "2020-11-15T15:41:04+00:00"
                ),
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                seen_at=datetime.fromisoformat("2020-02-01T15:41:04+00:00"),
                sorts_risk_level=-1,
            ),
            ToeLines(
                attacked_at=datetime.fromisoformat(
                    "2021-02-20T05:00:00+00:00"
                ),
                attacked_by="machine@fluidattacks.com",
                attacked_lines=1,
                be_present=True,
                be_present_until=None,
                comments="",
                filename="MyJar.class",
                first_attack_at=datetime.fromisoformat(
                    "2020-02-19T15:41:04+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer2@gmail.com",
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c5",
                loc=180,
                modified_date=datetime.fromisoformat(
                    "2020-11-15T15:41:04+00:00"
                ),
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                seen_at=datetime.fromisoformat("2020-02-01T15:41:04+00:00"),
                sorts_risk_level=-1,
            ),
            ToeLines(
                attacked_at=datetime.fromisoformat(
                    "2021-02-20T05:00:00+00:00"
                ),
                attacked_by="machine@fluidattacks.com",
                attacked_lines=30,
                be_present=True,
                be_present_until=None,
                comments="",
                filename="java_has_print_statements.java",
                first_attack_at=datetime.fromisoformat(
                    "2020-02-19T15:41:04+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer2@gmail.com",
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c5",
                loc=180,
                modified_date=datetime.fromisoformat(
                    "2020-11-15T15:41:04+00:00"
                ),
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                seen_at=datetime.fromisoformat("2020-02-01T15:41:04+00:00"),
                sorts_risk_level=-1,
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
