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
from db_model.events.enums import (
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidence,
    EventEvidences,
    EventState,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
    FindingEvidences,
    FindingState,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
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
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("solve_event")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "events": [
            {
                "event": Event(
                    id="418900971",
                    group_name="group1",
                    hacker=generic_data["global_vars"]["hacker_email"],
                    client="Fluid",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    description="ARM unit test",
                    type=EventType.OTHER,
                    event_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    evidences=EventEvidences(
                        image_1=EventEvidence(
                            file_name=(
                                "unittesting_418900971_evidence_image_1.png"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                        file_1=EventEvidence(
                            file_name=(
                                "unittesting_418900971_evidence_file_1.csv"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                    ),
                    state=EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T12:00:00+00:00"
                        ),
                        status=EventStateStatus.OPEN,
                    ),
                ),
                "historic_state": [
                    EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T19:40:05+00:00"
                        ),
                        status=EventStateStatus.CREATED,
                    ),
                ],
            },
            {
                "event": Event(
                    id="418900972",
                    group_name="group1",
                    hacker=generic_data["global_vars"]["hacker_email"],
                    client="Fluid",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    description="ARM unit test",
                    type=EventType.OTHER,
                    event_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    evidences=EventEvidences(
                        image_1=EventEvidence(
                            file_name=(
                                "unittesting_418900972_evidence_image_1.png"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                        file_1=EventEvidence(
                            file_name=(
                                "unittesting_418900972_evidence_file_1.csv"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                    ),
                    state=EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T12:00:00+00:00"
                        ),
                        status=EventStateStatus.OPEN,
                    ),
                ),
                "historic_state": [
                    EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T19:40:05+00:00"
                        ),
                        status=EventStateStatus.CREATED,
                    ),
                ],
            },
            {
                "event": Event(
                    id="418900973",
                    group_name="group1",
                    hacker=generic_data["global_vars"]["hacker_email"],
                    client="Fluid",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    description="ARM unit test",
                    type=EventType.OTHER,
                    event_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    evidences=EventEvidences(
                        image_1=EventEvidence(
                            file_name=(
                                "unittesting_418900973_evidence_image_1.png"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                        file_1=EventEvidence(
                            file_name=(
                                "unittesting_418900973_evidence_file_1.csv"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                    ),
                    state=EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T12:00:00+00:00"
                        ),
                        status=EventStateStatus.OPEN,
                    ),
                ),
                "historic_state": [
                    EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T19:40:05+00:00"
                        ),
                        status=EventStateStatus.CREATED,
                    ),
                ],
            },
            {
                "event": Event(
                    id="418900974",
                    group_name="group1",
                    hacker=generic_data["global_vars"]["hacker_email"],
                    client="Fluid",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    description="ARM unit test",
                    type=EventType.OTHER,
                    event_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    evidences=EventEvidences(
                        image_1=EventEvidence(
                            file_name=(
                                "unittesting_418900974_evidence_image_1.png"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                        file_1=EventEvidence(
                            file_name=(
                                "unittesting_418900974_evidence_file_1.csv"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                    ),
                    state=EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T12:00:00+00:00"
                        ),
                        status=EventStateStatus.OPEN,
                    ),
                ),
                "historic_state": [
                    EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T19:40:05+00:00"
                        ),
                        status=EventStateStatus.CREATED,
                    ),
                ],
            },
            {
                "event": Event(
                    id="418900975",
                    group_name="group1",
                    hacker=generic_data["global_vars"]["hacker_email"],
                    client="Fluid",
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    description="ARM unit test",
                    type=EventType.OTHER,
                    event_date=datetime.fromisoformat(
                        "2018-06-27T12:00:00+00:00"
                    ),
                    evidences=EventEvidences(
                        image_1=EventEvidence(
                            file_name=(
                                "unittesting_418900975_evidence_image_1.png"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                        file_1=EventEvidence(
                            file_name=(
                                "unittesting_418900975_evidence_file_1.csv"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2019-03-11T15:57:45+00:00"
                            ),
                        ),
                    ),
                    state=EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T12:00:00+00:00"
                        ),
                        status=EventStateStatus.OPEN,
                    ),
                ),
                "historic_state": [
                    EventState(
                        modified_by=generic_data["global_vars"][
                            "hacker_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2018-06-27T19:40:05+00:00"
                        ),
                        status=EventStateStatus.CREATED,
                    ),
                ],
            },
        ],
        "findings": [
            {
                "finding": Finding(
                    id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="unittesting",
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
                    evidences=FindingEvidences(),
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
                        modified_by="test2@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-01T00:45:12+00:00"
                        ),
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "4dbc03e0-4cfc-4b33-9b70-bb7566c460bd",
                        },
                    ),
                    FindingVerification(
                        comment_id="42343435",
                        modified_by="customer_manager@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-04T00:45:15+00:00"
                        ),
                        status=FindingVerificationStatus.ON_HOLD,
                        vulnerability_ids={
                            "4dbc03e0-4cfc-4b33-9b70-bb7566c460bd",
                        },
                    ),
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=0,
                    unreliable_open_vulnerabilities=1,
                ),
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.comm",
                    created_date=datetime.fromisoformat(
                        "2022-09-01T00:45:11+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="unittesting",
                    hacker_email="test1@gmail.com",
                    id="4dbc03e0-4cfc-4b33-9b70-bb7566c460bd",
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-09-01T00:45:11+00:00"
                        ),
                        source=Source.MACHINE,
                        specific="5",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="README.md",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2022-09-01T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                        unreliable_last_reattack_requester="test2@gmail.com",
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2022-09-01T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.ON_HOLD,
                        event_id="418900975",
                    ),
                    root_id="77637717-41d4-4242-854a-db8ff7fe5ed0",
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
