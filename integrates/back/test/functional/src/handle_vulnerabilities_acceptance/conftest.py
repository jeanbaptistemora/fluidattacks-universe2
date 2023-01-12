# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
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
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
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
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("handle_vulnerabilities_acceptance")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
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
                        evidence1=FindingEvidence(
                            description="evidence1",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence1",  # noqa: E501 pylint: disable=line-too-long
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        records=FindingEvidence(
                            description="records",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-records",  # noqa: E501 pylint: disable=line-too-long
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
                            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2020-12-26T05:45:00+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2020-02-24T05:45:00+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2018-04-01T05:45:00+00:00")
                    ),
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_where="192.168.1.2",
                ),
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:11+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.20",
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                ),
                "historic_treatment": [
                    VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    VulnerabilityTreatment(
                        assigned="user@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                        acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED,  # noqa: E501 pylint: disable=line-too-long
                    ),
                ],
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:11+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce9",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.20",
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                ),
                "historic_treatment": [
                    VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    VulnerabilityTreatment(
                        assigned="user@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                        acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED,  # noqa: E501 pylint: disable=line-too-long
                    ),
                ],
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:11+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdc10",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.20",
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                ),
                "historic_treatment": [
                    VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    VulnerabilityTreatment(
                        assigned="user@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                        acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED,  # noqa: E501 pylint: disable=line-too-long
                    ),
                ],
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:11+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdc11",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.20",
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                ),
                "historic_treatment": [
                    VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    VulnerabilityTreatment(
                        assigned="user@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                        acceptance_status=VulnerabilityAcceptanceStatus.SUBMITTED,  # noqa: E501 pylint: disable=line-too-long
                    ),
                ],
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
