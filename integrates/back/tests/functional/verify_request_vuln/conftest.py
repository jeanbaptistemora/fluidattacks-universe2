# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from back.tests import (
    db,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('verify_request_vuln')
@pytest.fixture(autouse=True, scope='session')
async def populate() -> bool:
    data: Dict[str, Any] = {
        'users': [
            {
                'email': 'test1@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
        ],
        'orgs': [
            {
                'name': 'orgtest',
                'id': '40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'users': [
                    'test1@gmail.com',
                ],
                'groups': [
                    'group1',
                ],
                'policy': {},
            },
        ],
        'groups': [
            {
                'project_name': 'group1',
                'description': '-',
                'language': 'en',
                'historic_configuration': [{
                    'date': '2020-05-20 17:00:00',
                    'has_drills': False,
                    'has_forces': False,
                    'requester': 'unknown',
                    'type': 'continuous',
                }],
                'project_status': 'ACTIVE',
            },
        ],
        'findings': [
            {
                'finding_id': '475041513',
                'project_name': 'group1',
                'files': [
                    {
                        'name': 'file1',
                        'description': 'description',
                        'file_url': 'route',
                    },
                ],
                'historic_state': [
                    {
                        'date': '2018-04-07 19:45:11',
                        'analyst': 'test1@gmail.com',
                        'source': 'source_path',
                        'state': 'APPROVED',
                    },
                ],
                'effect_solution': 'solution',
                'vulnerability': 'vulnerability',
                'analyst': 'test1@gmail.com',
                'cvss_version': '3.1',
                'exploitability': 0.94,
                'finding': 'FIN.H.060. Insecure exceptions',
                'cwe': '396',
                'finding_type': 'SECURITY',
                'requirements': 'R359. Avoid using generic exceptions.',
                'threat': 'Autenticated attacker from the Internet.',
                'affected_systems': 'test',
                'attack_vector_desc': 'Lose the traceability.',
                'availability_impact': 0.22,
                'availability_requirement': 1.5,
                'integrity_impact': 0.22,
                'integrity_requirement': 1,
                'related_findings': '0',
                'report_confidence': 1,
                'privileges_required': 0.62,
                'context': 'Cierre',
                'confidentiality_impact': 0.22,
                'remediation_level': 0.95,
                'attack_complexity': 0.44,
                'effect_solution': 'Implement',
                'resolution_level': 1,
                'cvss_temporal': 3.4,
                'modified_user_interaction': 0.62,
                'modified_integrity_impact': 0,
                'attack_vector': 0.2,
                'modified_attack_complexity': 0.44,
                'cvss_env': 1.7,
                'severity_scope': 1.2,
                'report_level': 'GENERAL',
                'confidence_level': 0.95,
                'modified_severity_scope': 0,
                'subscription': 'CONTINUOUS',
                'access_vector': 0.395,
                'modified_privileges_required': 0.27,
                'modified_attack_vector': 0.85,
                'scenario': 'ANONYMOUS_INTRANET',
                'records_number': '0',
                'finding_distribution': 0,
                'access_complexity': 0.61,
                'authentication': 0.56,
                'modified_confidentiality_impact': 0.22,
                'modified_availability_impact': 0.22,
                'collateral_damage_potential': 0.1,
                'test_type': 'APP',
                'actor': 'SOME_CUSTOMERS',
                'leader': 'aaa@gmail.com',
                'confidentiality_requirement': 0.5,
                'user_interaction': 0.85,
                'client_project': 'Unit Test',
                'cvss_basescore': 3.8,
                'interested': 'aaa@gmail.com',
            },
        ],
        'vulnerabilities': [
            {
                'finding_id': '475041513',
                'UUID': 'be09edb7-cd5c-47ed-bee4-97c645acdce8',
                'historic_state': [
                    {
                        'date': '2018-04-07 19:45:11',
                        'analyst': 'test1@gmail.com',
                        'source': 'integrates',
                        'state': 'open',
                        'approval_status': 'APPROVED',
                    },
                ],
                'historic_treatment': [
                    {
                        'date': '2018-04-07 19:45:11',
                        'treatment': 'NEW',
                    },
                ],
                'historic_verification': [
                    {
                        'date': '2018-04-08 19:45:11',
                        'status': 'REQUESTED',
                    },
                ],
                'vuln_type': 'ports',
                'where': '192.168.1.20',
                'specific': '9999',
            },
        ],
        'policies': [
            {
                'level': 'user',
                'subject': 'test1@gmail.com',
                'object': 'self',
                'role': 'admin',
            },
        ],
    }
    return await db.populate(data)
