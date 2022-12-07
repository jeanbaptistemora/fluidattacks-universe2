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
)
from db_model.findings.types import (
    Finding,
    FindingState,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_compliance")
@pytest.fixture(autouse=True, scope="session")
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
                "historic_verification": [],
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    created_by="test1@gmail.com",
                    created_date="2018-04-08T00:45:11+00:00",
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="3988168e-fc18-41f8-b219-2f33be09cc30",
                    state=VulnerabilityState(
                        modified_by="test1@gmail.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.CLOSED,
                        where="192.168.1.20",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="test1@gmail.com",
                    created_date="2018-04-08T00:45:11+00:00",
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="1a45b977-3f77-4bbe-8d3d-d43d6afd1383",
                    state=VulnerabilityState(
                        modified_by="test1@gmail.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        specific="2321",
                        status=VulnerabilityStateStatus.OPEN,
                        where="192.168.1.1",
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
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="test1@gmail.com",
                    created_date="2018-04-08T00:45:11+00:00",
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="d582d9fe-fa5d-4d5a-ab07-9372f51b1d9b",
                    state=VulnerabilityState(
                        modified_by="test1@gmail.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        specific="77777",
                        status=VulnerabilityStateStatus.OPEN,
                        where="192.168.1.7",
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
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    type=VulnerabilityType.PORTS,
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
                        status=VulnerabilityZeroRiskStatus.REJECTED,
                    ),
                ],
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date="2018-04-08T00:43:11+00:00",
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="37e6f824-1eae-441b-a12e-984bb4d84f86",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T00:43:11+00:00",
                        source=Source.ASM,
                        specific="4444",
                        status=VulnerabilityStateStatus.OPEN,
                        where="test1/test.sh",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:43:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_last_reattack_requester=(
                            "requester@gmail.com"
                        ),
                        unreliable_last_requested_reattack_date=(
                            "2018-04-08T01:45:11+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date="2018-04-08T01:45:11+00:00",
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date="2018-04-08T00:44:11+00:00",
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="51cf5f89-85e2-4cf9-a5b6-9cd8069124f7",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T00:44:11+00:00",
                        source=Source.ASM,
                        specific="4545",
                        status=VulnerabilityStateStatus.OPEN,
                        where="test2/test#.config",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:44:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_last_reattack_requester=(
                            "requester@gmail.com"
                        ),
                        unreliable_last_requested_reattack_date=(
                            "2018-04-08T01:45:11+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date="2018-04-08T01:45:11+00:00",
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                )
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@gmail.com",
                    created_date="2018-04-08T00:45:11+00:00",
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="hacker@gmail.com",
                    id="a859d449-0da2-4260-a05f-12089d756ab8",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    state=VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        specific="4646",
                        status=VulnerabilityStateStatus.CLOSED,
                        where="test3/test.sh",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.LINES,
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
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date="2018-04-08T01:45:12+00:00",
                        status=VulnerabilityVerificationStatus.VERIFIED,
                    ),
                ),
                "historic_state": [
                    VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.OPEN,
                        where="192.168.1.20",
                    ),
                    VulnerabilityState(
                        modified_by="hacker@gmail.com",
                        modified_date="2018-04-08T01:45:12+00:00",
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.CLOSED,
                        where="192.168.1.20",
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
