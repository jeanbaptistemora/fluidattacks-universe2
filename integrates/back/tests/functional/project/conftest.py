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
from dynamodb.types import (
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('project')
@pytest.fixture(autouse=True, scope='session')
async def populate() -> bool:
    data: Dict[str, Any] = {
        'users': [
            {
                'email': 'admin@gmail.com',
                'first_login': '',
                'first_name': '',
                'last_login': '',
                'last_name': '',
                'legal_remember': False,
                'phone_number': '-',
                'push_tokens': [],
                'is_registered': True,
            },
            {
                'email': 'analyst@gmail.com',
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
                    'admin@gmail.com',
                    'analyst@gmail.com',
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
                'description': 'this is group1',
                'language': 'en',
                'historic_configuration': [{
                    'date': '2020-05-20 17:00:00',
                    'has_drills': True,
                    'has_forces': True,
                    'requester': 'unknown',
                    'type': 'continuous',
                }],
                'project_status': 'ACTIVE',
                'closed_vulnerabilities': 1,
                'open_vulnerabilities': 1,
                'last_closing_date': 40,
                'max_open_severity': 4.3,
                'open_findings': 1,
                'mean_remediate': 2,
                'mean_remediate_low_severity': 3,
                'mean_remediate_medium_severity': 4,
                'tag': ['testing'],
            },
        ],
        'findings': [
            {
                'finding_id': '475041521',
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
                        'analyst': 'admin@gmail.com',
                        'source': 'source_path',
                        'state': 'APPROVED',
                    },
                ],
                'effect_solution': 'solution',
                'vulnerability': 'vulnerability',
                'analyst': 'admin@gmail.com',
                'cvss_version': '3.1',
                'exploitability': 0.94,
                'finding': 'FIN.H.060. Insecure exceptions',
                'cwe': '396',
                'finding_type': 'SECURITY',
                'requirements': 'R359. Avoid using generic exceptions.',
                'threat': 'Autenticated attacker from the Internet.',
                'affected_systems': 'system1',
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
            {
                'finding_id': '475041531',
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
                        'analyst': 'admin@gmail.com',
                        'source': 'source_path',
                        'state': 'CREATED',
                    },
                ],
                'effect_solution': 'solution',
                'vulnerability': 'vulnerability',
                'analyst': 'admin@gmail.com',
                'cvss_version': '3.1',
                'exploitability': 0.94,
                'finding': 'FIN.H.060. Insecure exceptions',
                'cwe': '396',
                'finding_type': 'SECURITY',
                'requirements': 'R359. Avoid using generic exceptions.',
                'threat': 'Autenticated attacker from the Internet.',
                'affected_systems': 'system2',
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
                'finding_id': '475041521',
                'UUID': 'be09edb7-cd5c-47ed-bee4-97c645acdce8',
                'historic_state': [
                    {
                        'date': '2018-04-07 19:45:11',
                        'analyst': 'admin@gmail.com',
                        'source': 'integrates',
                        'state': 'open',
                    },
                ],
                'historic_treatment': [
                    {
                        'date': '2018-04-07 19:45:11',
                        'treatment': 'NEW',
                    },
                ],
                'vuln_type': 'ports',
                'where': '192.168.1.20',
                'specific': '9999',
            },
            {
                'finding_id': '475041521',
                'UUID': '6401bc87-8633-4a4a-8d8e-7dae0ca57e6a',
                'historic_state': [
                    {
                        'date': '2018-04-07 19:45:11',
                        'analyst': 'admin@gmail.com',
                        'source': 'integrates',
                        'state': 'closed',
                    },
                ],
                'historic_treatment': [
                    {
                        'date': '2018-04-08 19:45:11',
                        'treatment_manager': 'anything@gmail.com',
                        'treatment': 'ACCEPTED',
                        'justification': 'justification',
                        'acceptance_date': '2018-04-08 19:45:11',
                        'user': 'anything@gmail.com',
                    },
                ],
                'vuln_type': 'ports',
                'where': '192.168.1.1',
                'specific': '2321',
            },
            {
                'finding_id': '475041531',
                'UUID': '6401bc87-8633-4a4a-8d8e-7dae0ca57e6a',
                'historic_state': [
                    {
                        'date': '2018-04-07 19:45:11',
                        'analyst': 'admin@gmail.com',
                        'source': 'integrates',
                        'state': 'open',
                    },
                ],
                'historic_treatment': [
                    {
                        'date': '2018-04-08 19:45:11',
                        'treatment_manager': 'anything@gmail.com',
                        'treatment': 'ACCEPTED',
                        'justification': 'justification',
                        'acceptance_date': '2018-04-08 19:45:11',
                        'user': 'anything@gmail.com',
                    },
                ],
                'vuln_type': 'ports',
                'where': '192.168.1.1',
                'specific': '2321',
            },
        ],
        'roots': (
            (
                'group1',
                GitRootItem(
                    cloning=GitRootCloning(
                        modified_date='2020-11-19T13:37:10+00:00',
                        reason='root creation',
                        status='UNKNOWN'
                    ),
                    id='63298a73-9dff-46cf-b42d-9b2f01a56690',
                    metadata=GitRootMetadata(
                        branch='master',
                        type='Git',
                        url='https://gitlab.com/fluidattacks/product'
                    ),
                    state=GitRootState(
                        environment_urls=[
                            'https://integrates.fluidattacks.com'
                        ],
                        environment='production',
                        gitignore=[
                            'bower_components/*',
                            'node_modules/*'
                        ],
                        includes_health_check=True,
                        modified_by='admin@gmail.com',
                        modified_date='2020-11-19T13:37:10+00:00',
                        nickname='',
                        status='ACTIVE'
                    )
                )
            ),
        ),
        'consultings': [
            {
                'content': 'This is a test comment',
                'created': '2019-05-28 15:09:37',
                'email': 'admin@gmail.com',
                'fullname': 'test one',
                'modified': '2019-05-28 15:09:37',
                'parent': 0,
                'project_name': 'group1',
                'user_id': 123456789,
            },
        ],
        'events': [
            {
                'accessibility': 'Repositorio',
                'action_after_blocking': 'EXECUTE_OTHER_PROJECT_SAME_CLIENT',
                'action_before_blocking': 'TEST_OTHER_PART_TOE',
                'analyst': 'unittest@fluidattacks.com',
                'client': 'Fluid',
                'client_project': 'group1',
                'closer': 'unittest',
                'context': 'FLUID',
                'detail': 'Integrates unit test',
                'event_id': '418900971',
                'historic_state': [
                    {
                        'analyst': 'unittest@fluidattacks.com',
                        'date': '2018-06-27 07:00:00',
                        'state': 'OPEN'
                    },
                    {
                        'analyst': 'unittest@fluidattacks.com',
                        'date': '2018-06-27 14:40:05',
                        'state': 'CREATED'
                    },
                ],
                'event_type': 'OTHER',
                'hours_before_blocking': '1',
                'project_name': 'group1',
                'subscription': 'ONESHOT',
            },
        ],
        'policies': [
            {
                'level': 'user',
                'subject': 'admin@gmail.com',
                'object': 'self',
                'role': 'admin',
            },
            {
                'level': 'group',
                'subject': 'admin@gmail.com',
                'object': 'group1',
                'role': 'group_manager',
            },
            {
                'level': 'user',
                'subject': 'analyst@gmail.com',
                'object': 'self',
                'role': 'user',
            },
            {
                'level': 'group',
                'subject': 'analyst@gmail.com',
                'object': 'group1',
                'role': 'analyst',
            },
            {
                'level': 'organization',
                'subject': 'analyst@gmail.com',
                'object': 'ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db',
                'role': 'customer',
            },
        ],
    }
    return await db.populate(data)
