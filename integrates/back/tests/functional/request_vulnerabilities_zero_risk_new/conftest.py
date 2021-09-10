from back.tests import (
    db,
)
from db_model.enums import (
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
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("request_vulnerabilities_zero_risk_new")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "findings_new": [
            {
                "finding": Finding(
                    id="475041513",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection - C Sharp SQL API",
                    compromised_attributes="Clave plana",
                    compromised_records=12,
                    risk="This is pytest created draft",
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
                    type="SECURITY",
                    requirements="REQ.0132. Passwords (phrase type) "
                    "must be at least 3 words long.",
                    threat="Updated threat",
                    affected_systems="Server bWAPP",
                    attack_vector_description="This is an updated attack vector",
                    scenario="UNAUTHORIZED_USER_EXTRANET",
                    evidences=FindingEvidences(
                        evidence1=FindingEvidence(
                            description="evidence1",
                            url="group1-475041513-evidence1",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        records=FindingEvidence(
                            description="records",
                            url="group1-475041513-records",
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
                        modified_by="test1@gmail.com",
                        modified_date="2020-01-01T00:45:12+00:00",
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_last_vulnerability=94,
                    unreliable_age=1,
                    unreliable_closed_vulnerabilities=1,
                    unreliable_is_verified=False,
                    unreliable_open_age=400,
                    unreliable_open_vulnerabilities=5,
                    unreliable_report_date="2018-04-01T05:45:00+00:00",
                    unreliable_status=FindingStatus.OPEN,
                ),
            },
        ],
        "vulnerabilities": [
            {
                "finding_id": "475041513",
                "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdce10",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "hacker@gmail.com",
                        "source": "asm",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "treatment": "NEW",
                    },
                ],
                "vuln_type": "ports",
                "where": "192.168.1.20",
                "specific": "9999",
            },
            {
                "finding_id": "475041513",
                "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdce11",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "hacker@gmail.com",
                        "source": "asm",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "treatment": "NEW",
                    },
                ],
                "vuln_type": "ports",
                "where": "192.168.1.20",
                "specific": "9999",
            },
            {
                "finding_id": "475041513",
                "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdce12",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "hacker@gmail.com",
                        "source": "asm",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "treatment": "NEW",
                    },
                ],
                "vuln_type": "ports",
                "where": "192.168.1.20",
                "specific": "9999",
            },
            {
                "finding_id": "475041513",
                "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdce13",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "hacker@gmail.com",
                        "source": "integrates",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "treatment": "NEW",
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.20",  # NOSONAR
                "specific": "9999",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
