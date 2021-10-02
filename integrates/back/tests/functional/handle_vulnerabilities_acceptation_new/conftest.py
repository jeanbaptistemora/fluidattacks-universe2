# flake8: noqa
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
@pytest.mark.resolver_test_group("handle_vulnerabilities_acceptation_new")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "findings_new": [
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
                    compromised_attributes="Clave plana",
                    compromised_records=12,
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
                    affected_systems="Server bWAPP",
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
                        modified_by="test1@gmail.com",
                        modified_date="2020-01-01T00:45:12+00:00",
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_is_verified=False,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date="2020-12-26T05:45:00+00:00",
                    unreliable_oldest_open_vulnerability_report_date="2020-02-24T05:45:00+00:00",
                    unreliable_oldest_vulnerability_report_date="2018-04-01T05:45:00+00:00",
                    unreliable_status=FindingStatus.OPEN,
                    unreliable_where="192.168.1.2",
                ),
            },
        ],
        "vulnerabilities": [
            {
                "finding_id": "3c475384-834c-47b0-ac71-a41a022e401c",
                "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "hacker@gmail.com",
                        "source": "asm",
                        "state": "open",
                        "approval_status": "APPROVED",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "treatment": "NEW",
                    },
                    {
                        "date": "2018-04-08 19:45:11",
                        "treatment": "ACCEPTED_UNDEFINED",
                        "acceptance_status": "SUBMITTED",
                    },
                ],
                "historic_verification": [
                    {
                        "date": "2018-04-08 19:45:11",
                        "status": "REQUESTED",
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.20",  # NOSONAR
                "specific": "9999",
            },
            {
                "finding_id": "3c475384-834c-47b0-ac71-a41a022e401c",
                "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdce9",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "hacker@gmail.com",
                        "source": "asm",
                        "state": "open",
                        "approval_status": "APPROVED",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "treatment": "NEW",
                    },
                    {
                        "date": "2018-04-08 19:45:11",
                        "treatment": "ACCEPTED_UNDEFINED",
                        "acceptance_status": "SUBMITTED",
                    },
                ],
                "historic_verification": [
                    {
                        "date": "2018-04-08 19:45:11",
                        "status": "REQUESTED",
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.20",  # NOSONAR
                "specific": "9999",
            },
            {
                "finding_id": "3c475384-834c-47b0-ac71-a41a022e401c",
                "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdc10",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "hacker@gmail.com",
                        "source": "asm",
                        "state": "open",
                        "approval_status": "APPROVED",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "treatment": "NEW",
                    },
                    {
                        "date": "2018-04-08 19:45:11",
                        "treatment": "ACCEPTED_UNDEFINED",
                        "acceptance_status": "SUBMITTED",
                    },
                ],
                "historic_verification": [
                    {
                        "date": "2018-04-08 19:45:11",
                        "status": "REQUESTED",
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.20",  # NOSONAR
                "specific": "9999",
            },
            {
                "finding_id": "3c475384-834c-47b0-ac71-a41a022e401c",
                "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdc11",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "hacker@gmail.com",
                        "source": "asm",
                        "state": "open",
                        "approval_status": "APPROVED",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "treatment": "NEW",
                    },
                    {
                        "date": "2018-04-08 19:45:11",
                        "treatment": "ACCEPTED_UNDEFINED",
                        "acceptance_status": "SUBMITTED",
                    },
                ],
                "historic_verification": [
                    {
                        "date": "2018-04-08 19:45:11",
                        "status": "REQUESTED",
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
