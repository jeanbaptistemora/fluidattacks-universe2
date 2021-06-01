from back.tests import (
    db,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("download_vuln_file")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "findings": [
            {
                "finding_id": "475041513",
                "project_name": "group1",
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
                        "analyst": "test1@gmail.com",
                        "source": "source_path",
                        "state": "APPROVED",
                    },
                ],
                "effect_solution": "solution",
                "vulnerability": "vulnerability",
                "analyst": "test1@gmail.com",
                "cvss_version": "3.1",
                "exploitability": 0.93,
                "finding": "FIN.H.060. Insecure exceptions",
                "cwe": "396",
                "finding_type": "SECURITY",
                "requirements": "R359. Avoid using generic exceptions.",
                "threat": "Autenticated attacker from the Internet.",
                "affected_systems": "test",
                "attack_vector_desc": "Lose the traceability.",
                "availability_impact": 0.21,
                "availability_requirement": 1.4,
                "integrity_impact": 0.22,
                "integrity_requirement": 1,
                "related_findings": "0",
                "report_confidence": 0.9,
                "privileges_required": 0.62,
                "context": "Cierre",
                "confidentiality_impact": 0.21,
                "remediation_level": 0.94,
                "attack_complexity": 0.43,
                "effect_solution": "Implement",
                "resolution_level": 0.9,
                "cvss_temporal": 3.3,
                "modified_user_interaction": 0.61,
                "modified_integrity_impact": 0.1,
                "attack_vector": 0.1,
                "modified_attack_complexity": 0.3,
                "cvss_env": 1.6,
                "severity_scope": 1.1,
                "report_level": "GENERAL",
                "confidence_level": 0.94,
                "modified_severity_scope": 0,
                "subscription": "CONTINUOUS",
                "access_vector": 0.394,
                "modified_privileges_required": 0.26,
                "modified_attack_vector": 0.84,
                "scenario": "ANONYMOUS_INTRANET",
                "records_number": "0",
                "finding_distribution": 0,
                "access_complexity": 0.6,
                "authentication": 0.55,
                "modified_confidentiality_impact": 0.21,
                "modified_availability_impact": 0.21,
                "collateral_damage_potential": 0.11,
                "test_type": "APP",
                "actor": "SOME_CUSTOMERS",
                "leader": "aaa@gmail.com",
                "confidentiality_requirement": 0.51,
                "user_interaction": 0.84,
                "client_project": "Unit Test",
                "cvss_basescore": 3.9,
                "interested": "aaa@gmail.com",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
