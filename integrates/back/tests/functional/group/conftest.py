from back.tests import (
    db,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
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
        "findings": [
            {
                "finding_id": "475041521",
                "group_name": "group1",
                "files": [
                    {
                        "name": "file1",
                        "description": "description",
                        "file_url": "route",
                    },
                ],
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": generic_data["global_vars"]["admin_email"],
                        "source": "source_path",
                        "state": "APPROVED",
                    },
                ],
                "effect_solution": "solution",
                "vulnerability": "vulnerability",
                "analyst": generic_data["global_vars"]["admin_email"],
                "cvss_version": "3.1",
                "exploitability": 0.94,
                "finding": "060. Insecure exceptions",
                "requirements": "R359. Avoid using generic exceptions.",
                "threat": "Autenticated attacker from the Internet.",
                "affected_systems": "system1",
                "attack_vector_desc": "Lose the traceability.",
                "availability_impact": 0.22,
                "availability_requirement": 1.5,
                "integrity_impact": 0.22,
                "integrity_requirement": 1,
                "related_findings": "0",
                "report_confidence": 1,
                "privileges_required": 0.62,
                "context": "Cierre",
                "confidentiality_impact": 0.22,
                "remediation_level": 0.95,
                "attack_complexity": 0.44,
                "resolution_level": 1,
                "cvss_temporal": 3.4,
                "modified_user_interaction": 0.62,
                "modified_integrity_impact": 0,
                "attack_vector": 0.2,
                "modified_attack_complexity": 0.44,
                "cvss_env": 1.7,
                "severity_scope": 1.2,
                "report_level": "GENERAL",
                "confidence_level": 0.95,
                "modified_severity_scope": 0,
                "subscription": "CONTINUOUS",
                "access_vector": 0.395,
                "modified_privileges_required": 0.27,
                "modified_attack_vector": 0.85,
                "records_number": "0",
                "finding_distribution": 0,
                "access_complexity": 0.61,
                "authentication": 0.56,
                "modified_confidentiality_impact": 0.22,
                "modified_availability_impact": 0.22,
                "collateral_damage_potential": 0.1,
                "test_type": "APP",
                "leader": "aaa@gmail.com",
                "confidentiality_requirement": 0.5,
                "user_interaction": 0.85,
                "client_project": "Unit Test",
                "cvss_basescore": 3.8,
                "interested": "bbb@gmail.com",
            },
            {
                "finding_id": "475041531",
                "group_name": "group1",
                "files": [
                    {
                        "name": "file1",
                        "description": "description",
                        "file_url": "route",
                    },
                ],
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:12",
                        "analyst": generic_data["global_vars"]["admin_email"],
                        "source": "source_path",
                        "state": "CREATED",
                    },
                ],
                "effect_solution": "solution",
                "vulnerability": "vulnerability",
                "analyst": generic_data["global_vars"]["admin_email"],
                "cvss_version": "3.1",
                "exploitability": 0.94,
                "finding": "060. Insecure exceptions",
                "requirements": "R359. Avoid using generic exceptions.",
                "threat": "Autenticated attacker from the Internet.",
                "affected_systems": "system2",
                "attack_vector_desc": "Lose the traceability.",
                "availability_impact": 0.22,
                "availability_requirement": 1.5,
                "integrity_impact": 0.22,
                "integrity_requirement": 1,
                "related_findings": "0",
                "report_confidence": 1,
                "privileges_required": 0.62,
                "context": "Cierre",
                "confidentiality_impact": 0.22,
                "remediation_level": 0.95,
                "attack_complexity": 0.44,
                "resolution_level": 1,
                "cvss_temporal": 3.4,
                "modified_user_interaction": 0.62,
                "modified_integrity_impact": 0,
                "attack_vector": 0.2,
                "modified_attack_complexity": 0.44,
                "cvss_env": 1.7,
                "severity_scope": 1.2,
                "report_level": "GENERAL",
                "confidence_level": 0.95,
                "modified_severity_scope": 0,
                "subscription": "CONTINUOUS",
                "access_vector": 0.395,
                "modified_privileges_required": 0.27,
                "modified_attack_vector": 0.85,
                "records_number": "0",
                "finding_distribution": 0,
                "access_complexity": 0.61,
                "authentication": 0.56,
                "modified_confidentiality_impact": 0.22,
                "modified_availability_impact": 0.22,
                "collateral_damage_potential": 0.1,
                "test_type": "APP",
                "leader": "ccc@gmail.com",
                "confidentiality_requirement": 0.5,
                "user_interaction": 0.85,
                "client_project": "Unit Test",
                "cvss_basescore": 3.8,
                "interested": "ddd@gmail.com",
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
