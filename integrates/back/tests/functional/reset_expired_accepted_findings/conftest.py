# flake8: noqa
from back.tests import (
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
    Finding31Severity,
    FindingState,
    FindingStatus,
    FindingUnreliableIndicatorsToUpdate,
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
@pytest.mark.resolver_test_group("reset_expired_accepted_findings")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "groups": [
            {
                "project_name": "acme",
                "description": "ASM test group",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2021-07-01 00:00:00",
                        "has_drills": True,
                        "has_forces": True,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "project_status": "ACTIVE",
                "closed_vulnerabilities": 1,
                "open_vulnerabilities": 1,
                "last_closing_date": 40,
                "max_open_severity": 4.3,
                "open_findings": 1,
                "mean_remediate": 2,
                "mean_remediate_low_severity": 3,
                "mean_remediate_medium_severity": 4,
                "tag": ["testing"],
            },
        ],
        "findings_new": [
            {
                "finding": Finding(
                    id="475041521",
                    group_name="acme",
                    state=FindingState(
                        modified_by="hacker@gmail.com",
                        modified_date="2021-07-01T00:01:00+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="060. Insecure exceptions",
                    compromised_attributes="Clave plana",
                    compromised_records=12,
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email="admin@gmail.com",
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
                    requirements="R359. Avoid using generic exceptions.",
                    threat="Autenticated attacker from the Internet.",
                    affected_systems="system1",
                    attack_vector_description="This is an updated attack vector",
                ),
                "historic_state": [
                    FindingState(
                        modified_by="hacker@gmail.com",
                        modified_date="2021-07-01T00:01:01+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="hacker@gmail.com",
                        modified_date="2021-07-01T00:01:02+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                    ),
                    FindingState(
                        modified_by="hacker@gmail.com",
                        modified_date="2021-07-01T00:01:03+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="admin@gmail.com",
                        modified_date="2021-07-01T00:01:04+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                    ),
                ],
                "historic_verification": [],
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
                "finding_id": "475041521",
                "UUID": "6401bc87-8633-4a4a-8d8e-7dae0ca57e61",
                "historic_state": [
                    {
                        "date": "2021-07-01 00:02:00",
                        "analyst": "admin@gmail.com",
                        "source": "asm",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2021-07-01 00:02:00",
                        "treatment": "NEW",
                    },
                    {
                        "date": "2021-07-01 00:02:01",
                        "treatment_manager": "hacker@gmail.com",
                        "treatment": "ACCEPTED",
                        "justification": "justification",
                        "acceptance_date": "2021-08-01 00:02:00",
                        "user": "hacker@gmail.com",
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.1",  # NOSONAR
                "specific": "1111",
            },
            {
                "finding_id": "475041521",
                "UUID": "6401bc87-8633-4a4a-8d8e-7dae0ca57e62",
                "historic_state": [
                    {
                        "date": "2021-07-01 00:02:00",
                        "analyst": "admin@gmail.com",
                        "source": "asm",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2021-07-01 00:02:00",
                        "treatment": "NEW",
                    },
                    {
                        "date": "2021-07-01 00:02:01",
                        "treatment_manager": "hacker@gmail.com",
                        "treatment": "ACCEPTED_UNDEFINED",
                        "justification": "justification",
                        "acceptance_status": "SUBMITTED",
                        "user": "hacker@gmail.com",
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.1",  # NOSONAR
                "specific": "2222",
            },
            {
                "finding_id": "475041521",
                "UUID": "6401bc87-8633-4a4a-8d8e-7dae0ca57e63",
                "historic_state": [
                    {
                        "date": "2021-07-01 00:02:00",
                        "analyst": "admin@gmail.com",
                        "source": "asm",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2021-07-01 00:02:00",
                        "treatment": "NEW",
                    },
                    {
                        "date": "2021-08-09 00:02:01",
                        "treatment_manager": "hacker@gmail.com",
                        "treatment": "ACCEPTED_UNDEFINED",
                        "justification": "justification",
                        "acceptance_status": "SUBMITTED",
                        "user": "hacker@gmail.com",
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.1",  # NOSONAR
                "specific": "3333",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
