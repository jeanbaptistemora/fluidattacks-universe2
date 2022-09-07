# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# flake8: noqa
from back.test import (
    db,
)
from db_model.enums import (
    Source,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
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
    FindingTreatmentSummary,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
    FindingVerificationSummary,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityZeroRisk,
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
@pytest.mark.resolver_test_group("finding")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "findings": [
            {
                "finding": Finding(
                    id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    evidences=FindingEvidences(
                        evidence1=FindingEvidence(
                            description="evidence1",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence1",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        evidence2=FindingEvidence(
                            description="evidence2",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence2",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        evidence3=FindingEvidence(
                            description="evidence3",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence3",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        evidence4=FindingEvidence(
                            description="evidence4",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence4",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        evidence5=FindingEvidence(
                            description="evidence5",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence5",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        exploitation=FindingEvidence(
                            description="exploitation",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-exploitation",
                            modified_date="2010-11-19T13:37:10+00:00",
                        ),
                        animation=FindingEvidence(
                            description="animation",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-animation",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                    ),
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
                    min_time_to_remediate=4,
                    requirements=(
                        "REQ.0132. Passwords (phrase type) "
                        "must be at least 3 words long."
                    ),
                    threat="Updated threat",
                    attack_vector_description=(
                        "This is an updated attack vector"
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
                            "uuid2",
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
                    unreliable_treatment_summary=FindingTreatmentSummary(
                        accepted=1,
                        accepted_undefined=2,
                        in_progress=3,
                        new=4,
                    ),
                    unreliable_verification_summary=FindingVerificationSummary(
                        requested=1, on_hold=2, verified=3
                    ),
                    unreliable_where="192.168.1.2",
                ),
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                    specific="9999",
                    state=VulnerabilityState(
                        modified_by="test1@gmail.com",
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
                        unreliable_report_date="2018-04-08T00:45:11+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    where="192.168.1.20",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="6401bc87-8633-4a4a-8d8e-7dae0ca57e6a",
                    specific="2321",
                    state=VulnerabilityState(
                        modified_by="test1@gmail.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        accepted_until="2018-04-09T00:45:11+00:00",
                        justification="justification",
                        assigned="anything@gmail.com",
                        modified_by="anything@gmail.com",
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2018-04-08T00:45:11+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    where="192.168.1.1",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="7771bc87-8633-4a4a-8d8e-7dae0ca57e7a",
                    specific="77777",
                    state=VulnerabilityState(
                        modified_by="test1@gmail.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        accepted_until="2018-04-09T00:45:11+00:00",
                        justification="justification",
                        assigned="anything@gmail.com",
                        modified_by="anything@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2018-04-08T00:45:11+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    type=VulnerabilityType.PORTS,
                    where="192.168.1.7",
                ),
                "historic_zero_risk": [
                    VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="requested@zr.com",
                        modified_date="2018-09-28T15:32:58+00:00",
                        status=VulnerabilityZeroRiskStatus.REQUESTED,
                    ),
                    VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="confirmed@zr.com",
                        modified_date="2020-09-09T21:01:26+00:00",
                        status=VulnerabilityZeroRiskStatus.CONFIRMED,
                    ),
                ],
            },
        ],
        "finding_comments": [
            {
                "finding_comment": FindingComment(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    id="43455343453",
                    comment_type=CommentType.OBSERVATION,
                    content="This is a test observations",
                    email="admin@gmail.com",
                    full_name="test one",
                    creation_date="2019-05-28T20:09:37+00:00",
                    parent_id="0",
                )
            },
            {
                "finding_comment": FindingComment(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    id="42343434",
                    comment_type=CommentType.COMMENT,
                    content="This is a test observations",
                    email="admin@gmail.com",
                    full_name="test one",
                    creation_date="2019-05-28T20:09:37+00:00",
                    parent_id="0",
                )
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
