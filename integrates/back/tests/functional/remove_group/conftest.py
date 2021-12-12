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
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
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
@pytest.mark.resolver_test_group("remove_group")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "groups": [
            {
                "project_name": "group1",
                "description": "-",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_drills": False,
                        "has_forces": False,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "project_status": "ACTIVE",
            },
            {
                "project_name": "group2",
                "description": "-",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_drills": False,
                        "has_forces": False,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "project_status": "ACTIVE",
            },
        ],
        "findings": [
            {
                "finding": Finding(
                    id="8888888888",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="F001. Draft",
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
                        animation=FindingEvidence(
                            description="animation",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence1",
                            modified_date="2020-11-19T13:50:10+00:00",
                        ),
                    ),
                ),
                "historic_state": [],
                "historic_verification": [
                    FindingVerification(
                        comment_id="42343434",
                        modified_by="test1@gmail.com",
                        modified_date="2020-04-08T00:46:12+00:00",
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
            {
                "finding": Finding(
                    id="475041521",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="F002. Very serious vulnerability",
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
                        evidence2=FindingEvidence(
                            description="evidence2",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence1",
                            modified_date="2020-11-19T13:50:10+00:00",
                        ),
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:12+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                    ),
                ],
                "historic_verification": [
                    FindingVerification(
                        comment_id="42343434",
                        modified_by="test1@gmail.com",
                        modified_date="2020-04-08T00:46:12+00:00",
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
            {
                "finding": Finding(
                    id="475041531",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="F003. Deleted",
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
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:12+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.DELETED,
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
                "vulnerability": Vulnerability(
                    finding_id="475041521",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                    specific="9999",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2018-04-08T00:45:13+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:45:14+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.PORTS,
                    where="192.168.1.20",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="475041521",
                    id="6401bc87-8633-4a4a-8d8e-7dae0ca57e6a",
                    specific="2321",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2018-04-08T00:45:15+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.CLOSED,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        accepted_until="2018-04-09T00:45:11+00:00",
                        justification="justification",
                        assigned=generic_data["global_vars"]["hacker_email"],
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                    ),
                    type=VulnerabilityType.PORTS,
                    where="192.168.1.1",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="475041531",
                    id="6401bc87-8633-4a4a-8d8e-7dae0ca57e6a",
                    specific="2321",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2018-04-08T00:45:15+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        accepted_until="2018-04-09T00:45:11+00:00",
                        justification="justification",
                        assigned=generic_data["global_vars"]["hacker_email"],
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                    ),
                    type=VulnerabilityType.PORTS,
                    where="192.168.1.1",
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
