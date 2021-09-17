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
@pytest.mark.resolver_test_group("upload_file")
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
                        "analyst": "admin@gmail.com",
                        "source": "source_path",
                        "state": "APPROVED",
                    },
                ],
                "vulnerability": "vulnerability",
                "analyst": "admin@gmail.com",
                "cvss_version": "3.1",
                "exploitability": 0.94,
                "finding": "060. Insecure exceptions",
                "finding_type": "SECURITY",
                "requirements": "R359. Avoid using generic exceptions.",
                "threat": "Autenticated attacker from the Internet.",
                "affected_systems": "test",
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
                "effect_solution": "Implement",
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
                "scenario": "ANONYMOUS_INTRANET",
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
                "interested": "aaa@gmail.com",
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
                    nickname="product",
                    other=None,
                    reason=None,
                    status="ACTIVE",
                    url="https://gitlab.com/fluidattacks/product",
                ),
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
