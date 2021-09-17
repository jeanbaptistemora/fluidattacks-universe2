from back.tests import (
    db,
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
                "finding_id": "475041513",
                "group_name": "group1",
                "files": [
                    {
                        "name": "evidence_route_1",
                        "description": "evidence1",
                        "file_url": "group1-475041513-evidence1",
                        "upload_date": "2021-03-16 13:58:41",
                    },
                    {
                        "name": "",
                        "description": "evidence2",
                        "file_url": "",
                        "upload_date": "2021-03-16 13:58:41",
                    },
                    {
                        "name": "evidence_route_3",
                        "description": "evidence3",
                        "file_url": "group1-475041513-evidence3",
                        "upload_date": "2021-03-16 13:58:41",
                    },
                    {
                        "name": "evidence_route_4",
                        "description": "evidence4",
                        "file_url": "group1-475041513-evidence4",
                        "upload_date": "2021-03-16 13:58:41",
                    },
                    {
                        "name": "evidence_route_5",
                        "description": "evidence5",
                        "file_url": "group1-475041513-evidence5",
                        "upload_date": "2021-03-16 13:58:41",
                    },
                    {
                        "name": "evidence_route_6",
                        "description": "evidence6",
                        "file_url": "group1-475041513-evidence6",
                        "upload_date": "2021-03-16 13:58:41",
                    },
                    {
                        "name": "animation",
                        "description": "animation",
                        "file_url": "group1-475041513-animation",
                        "upload_date": "2021-03-16 13:58:41",
                    },
                ],
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "test1@gmail.com",
                        "source": "source_path",
                        "state": "APPROVED",
                    },
                ],
                "title": "001. SQL injection - C Sharp SQL API",
                "compromised_attributes": "Clave plana",
                "bts": "",
                "vulnerability": "I just have updated the description",
                "analyst": "test1@gmail.com",
                "cvss_version": "3.1",
                "exploitability": 0.94,
                "finding": "001. SQL injection - C Sharp SQL API",
                "finding_type": "SECURITY",
                "requirements": "REQ.0132. Passwords (phrase type) "
                "must be at least 3 words long.",
                "threat": "Updated threat",
                "affected_systems": "Server bWAPP",
                "attack_vector_desc": "This is an updated attack vector",
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
                "effect_solution": "Updated recommendation",
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
                "scenario": "UNAUTHORIZED_USER_EXTRANET",
                "records_number": "12",
                "records": "Clave plana",
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
                "interested": "aaa@gmail.com",
            },
        ],
        "vulnerabilities": [
            {
                "finding_id": "475041513",
                "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "test1@gmail.com",
                        "source": "asm",
                        "state": "closed",
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
                "UUID": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6a",
                "historic_state": [
                    {
                        "date": "2018-04-07 19:45:11",
                        "analyst": "test1@gmail.com",
                        "source": "asm",
                        "state": "open",
                    },
                ],
                "historic_treatment": [
                    {
                        "date": "2018-04-08 19:45:11",
                        "treatment_manager": "anything@gmail.com",
                        "treatment": "ACCEPTED",
                        "justification": "justification",
                        "acceptance_date": "2018-04-08 19:45:11",
                        "user": "anything@gmail.com",
                    },
                ],
                "vuln_type": "ports",
                "where": "192.168.1.1",
                "specific": "2321",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
