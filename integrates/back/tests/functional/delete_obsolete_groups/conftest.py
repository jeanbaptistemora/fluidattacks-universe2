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
@pytest.mark.resolver_test_group("delete_obsolete_groups")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "orgs": [
            {
                "name": "orgtest",
                "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                "users": [
                    "admin@gmail.com",
                ],
                "groups": [
                    "group1",
                    "setpendingdeletion",
                    "deletegroup",
                ],
                "policy": {
                    "max_acceptance_days": 90,
                    "max_number_acceptations": 4,
                    "max_acceptance_severity": 7,
                    "min_acceptance_severity": 3,
                    "historic_max_number_acceptations": [
                        {
                            "date": "2019-11-22 15:07:57",
                            "user": "test1@gmail.com",
                            "max_number_acceptations": 4,
                        },
                    ],
                },
            },
        ],
        "groups": [
            {
                "project_name": "group1",
                "description": "ASM group",
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
                "open_vulnerabilities": 1,
                "last_closing_date": 40,
                "max_open_severity": 4.3,
                "open_findings": 1,
                "mean_remediate": 2,
                "mean_remediate_low_severity": 3,
                "mean_remediate_medium_severity": 4,
                "tag": ["testing"],
            },
            {
                "project_name": "setpendingdeletion",
                "description": "ASM group",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_drills": False,
                        "has_forces": False,
                        "has_skims": False,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "total_treatment": {
                    "accepted": 2,
                    "inProgress": 1,
                    "undefined": 0,
                },
                "environments": [],
                "files": [],
                "project_status": "SUSPENDED",
                "closed_vulnerabilities": 0,
                "open_vulnerabilities": 0,
                "last_closing_date": 12,
                "last_closing_vuln_finding": "",
                "max_open_severity": 4.9,
                "max_open_severity_finding": "",
                "open_findings": 0,
                "mean_remediate": 100,
                "mean_remediate_low_severity": 0,
                "mean_remediate_medium_severity": 0,
                "mean_remediate_high_severity": 0,
                "mean_remediate_critical_severity": 0,
                "remediated_over_time": [],
                "repositories": [],
                "tag": ["test-projects"],
            },
            {
                "project_name": "deletegroup",
                "description": "ASM group",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_drills": False,
                        "has_forces": False,
                        "has_skims": False,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "total_treatment": {
                    "accepted": 2,
                    "inProgress": 1,
                    "undefined": 0,
                },
                "environments": [],
                "files": [],
                "project_status": "ACTIVE",
                "closed_vulnerabilities": 0,
                "open_vulnerabilities": 0,
                "last_closing_date": 12,
                "last_closing_vuln_finding": "",
                "max_open_severity": 4.9,
                "max_open_severity_finding": "",
                "open_findings": 0,
                "mean_remediate": 100,
                "mean_remediate_low_severity": 0,
                "mean_remediate_medium_severity": 0,
                "mean_remediate_high_severity": 0,
                "mean_remediate_critical_severity": 0,
                "remediated_over_time": [],
                "repositories": [],
                "tag": ["test-projects"],
                "pending_deletion_date": "2020-12-22 14:36:29",
            },
        ],
        "findings_new": [
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
                    title="060. Insecure exceptions",
                    compromised_attributes="Clave plana",
                    compromised_records=12,
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
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
