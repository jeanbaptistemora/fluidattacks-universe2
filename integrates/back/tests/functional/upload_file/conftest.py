# flake8: noqa
from back.tests import (
    db,
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
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootState,
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
@pytest.mark.resolver_test_group("upload_file")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "findings": [
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
                    requirements="REQ.0132. Passwords (phrase type) "
                    "must be at least 3 words long.",
                    threat="Updated threat",
                    attack_vector_description="This is an updated attack vector",
                    evidences=FindingEvidences(
                        evidence1=FindingEvidence(
                            description="evidence1",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence1",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        records=FindingEvidence(
                            description="records",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-records",
                            modified_date="2111-11-19T13:37:10+00:00",
                        ),
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:12+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:13+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:14+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2018-04-08T00:45:11+00:00",
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
                    unreliable_is_verified=True,
                    unreliable_open_vulnerabilities=2,
                    unreliable_newest_vulnerability_report_date="2018-04-08T00:45:11+00:00",
                    unreliable_oldest_open_vulnerability_report_date="2018-04-08T00:43:11+00:00",
                    unreliable_oldest_vulnerability_report_date="2018-04-08T00:43:11+00:00",
                    unreliable_status=FindingStatus.OPEN,
                    unreliable_where="192.168.1.44, 192.168.1.45, 192.168.1.46",
                ),
            },
        ],
        "roots": (
            GitRootItem(
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
                        GitEnvironmentUrl(url="https://test.com")
                    ],
                    gitignore=["bower_components/*", "node_modules/*"],
                    includes_health_check=True,
                    modified_by="admin@gmail.com",
                    modified_date="2020-11-19T13:37:10+00:00",
                    nickname="product",
                    other=None,
                    reason=None,
                    status="ACTIVE",
                    url="https://gitlab.com/fluidattacks/product",
                ),
                type="Git",
            ),
        ),
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                    repo="product",
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
                        unreliable_last_reattack_requester="requester@gmail.com",
                        unreliable_last_requested_reattack_date="2018-04-08T01:45:11+00:00",
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
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce9",
                    repo="product",
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
                        unreliable_last_reattack_requester="requester@gmail.com",
                        unreliable_last_requested_reattack_date="2018-04-08T01:45:11+00:00",
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
                    id="be09edb7-cd5c-47ed-bee4-97c645acdcea",
                    repo="product",
                    specific="4646",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T00:45:11+01:00",
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
                        unreliable_last_reattack_date="2018-04-08T01:45:12+00:00",
                        unreliable_last_reattack_requester="requester@gmail.com",
                        unreliable_last_requested_reattack_date="2018-04-08T01:45:11+00:00",
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
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
