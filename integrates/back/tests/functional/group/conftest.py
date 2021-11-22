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
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
    MachineGitRootExecution,
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
@pytest.mark.resolver_test_group("group")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "groups": [
            {
                "project_name": "group1",
                "description": "this is group1",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_drills": True,
                        "has_forces": True,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "project_status": "ACTIVE",
                "closed_vulnerabilities": 1,
                "open_vulnerabilities": 2,
                "last_closing_date": 40,
                "last_closing_vuln_finding": "475041521",
                "max_open_severity": 4.3,
                "max_open_severity_finding": "475041521",
                "open_findings": 2,
                "mean_remediate": 2,
                "mean_remediate_low_severity": 3,
                "mean_remediate_medium_severity": 4,
                "tag": ["testing"],
            },
        ],
        "findings": [
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
                    title="060. Insecure service configuration - Host verification",
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email=generic_data["global_vars"]["admin_email"],
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
                        modified_by=generic_data["global_vars"]["admin_email"],
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
                    id="575041531",
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
                        attack_complexity=Decimal("0.1"),
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
                    affected_systems="system2",
                    attack_vector_description="This is an updated attack vector",
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
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2018-04-08T00:45:11+00:00",
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
            {
                "finding": Finding(
                    id="475041531",
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
                        attack_complexity=Decimal("0.1"),
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
                    affected_systems="system2",
                    attack_vector_description="This is an updated attack vector",
                ),
                "historic_state": [],
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
                "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:13",
                        "analyst": generic_data["global_vars"]["admin_email"],
                        "source": "asm",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-07 19:45:14",
                        "treatment": "NEW",
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.20",  # NOSONAR
                "specific": "9999",
            },
            {
                "finding_id": "475041521",
                "UUID": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6a",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:15",
                        "analyst": generic_data["global_vars"]["admin_email"],
                        "source": "asm",
                        "state": "closed",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-08 19:45:11",
                        "treatment_manager": generic_data["global_vars"][
                            "hacker_email"
                        ],
                        "treatment": "ACCEPTED",
                        "justification": "justification",
                        "acceptance_date": "2018-04-08 19:45:11",
                        "user": generic_data["global_vars"]["hacker_email"],
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.1",  # NOSONAR
                "specific": "2321",
            },
            {
                "finding_id": "575041531",
                "UUID": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6b",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:16",
                        "analyst": generic_data["global_vars"]["admin_email"],
                        "source": "integrates",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-08 19:45:11",
                        "treatment_manager": generic_data["global_vars"][
                            "hacker_email"
                        ],
                        "treatment": "ACCEPTED",
                        "justification": "justification",
                        "acceptance_date": "2018-04-08 19:45:11",
                        "user": generic_data["global_vars"]["hacker_email"],
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.1",  # NOSONAR
                "specific": "2321",
            },
            {
                "finding_id": "475041531",
                "UUID": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6a",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:16",
                        "analyst": generic_data["global_vars"]["admin_email"],
                        "source": "asm",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-08 19:45:11",
                        "treatment_manager": generic_data["global_vars"][
                            "hacker_email"
                        ],
                        "treatment": "ACCEPTED",
                        "justification": "justification",
                        "acceptance_date": "2018-04-08 19:45:11",
                        "user": generic_data["global_vars"]["hacker_email"],
                    },
                ],
                "vuln_type": "ports",
                # FP: local testing
                "where": "192.168.1.1",  # NOSONAR
                "specific": "2321",
            },
        ],
        "roots": (
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2020-11-19T13:37:10+00:00",
                    reason="root creation",
                    status="UNKNOWN",
                ),
                group_name="group1",
                id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                machine_execution=MachineGitRootExecution(
                    queue_date="2021-10-08T16:58:12.499243",
                    finding_code="F122",
                    job_id="78c546bh-dgf5-47e4-a7b3-4a1ebbsd0623",
                ),
                metadata=GitRootMetadata(type="Git"),
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
                    nickname="",
                    other=None,
                    reason=None,
                    status="ACTIVE",
                    url="https://gitlab.com/fluidattacks/product",
                ),
            ),
        ),
        "consultings": [
            {
                "content": "This is a test comment",
                "created": "2019-05-28 15:09:37",
                "email": "admin@gmail.com",
                "fullname": "test one",
                "modified": "2019-05-28 15:09:37",
                "parent": 0,
                "group_name": "group1",
                "user_id": 123456789,
            },
        ],
        "events": [
            {
                "accessibility": "Repositorio",
                "action_after_blocking": "EXECUTE_OTHER_GROUP_SAME_CLIENT",
                "action_before_blocking": "TEST_OTHER_PART_TOE",
                "analyst": generic_data["global_vars"]["hacker_email"],
                "client": "Fluid",
                "client_project": "group1",
                "closer": "unittest",
                "context": "FLUID",
                "detail": "ASM unit test",
                "event_id": "418900971",
                "historic_state": [
                    {
                        "analyst": generic_data["global_vars"]["hacker_email"],
                        "date": "2018-06-27 07:00:00",
                        "state": "OPEN",
                    },
                    {
                        "analyst": generic_data["global_vars"]["hacker_email"],
                        "date": "2018-06-27 14:40:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "hours_before_blocking": "1",
                "group_name": "group1",
                "subscription": "ONESHOT",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
