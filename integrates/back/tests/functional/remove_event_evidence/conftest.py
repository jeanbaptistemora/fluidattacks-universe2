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
@pytest.mark.resolver_test_group('remove_event_evidence')
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
            {
                'email': 'closer@gmail.com',
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
                    'closer@gmail.com',
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
        'events': [
            {
                'project_name': 'group1',
                'event_id': '418900971',
                'accessibility': 'Repositorio',
                'affected_components': 'affected_components_test',
                'action_after_blocking': 'EXECUTE_OTHER_PROJECT_SAME_CLIENT',
                'action_before_blocking': 'TEST_OTHER_PART_TOE',
                'analyst': 'unittest@fluidattacks.com',
                'client': 'Fluid',
                'client_project': 'group1',
                'closer': 'unittest',
                'closing_date': '2018-06-27 14:40:05',
                'context': 'FLUID',
                'detail': 'Integrates unit test1',
                'historic_state': [
                    {
                        'analyst': 'unittest@fluidattacks.com',
                        'date': '2018-06-27 07:00:00',
                        'state': 'OPEN',
                    },
                    {
                        'analyst': 'unittest@fluidattacks.com',
                        'date': '2018-06-27 14:40:05',
                        'state': 'CREATED',
                    },
                ],
                'event_type': 'OTHER',
                'hours_before_blocking': '1',
                'subscription': 'ONESHOT',
                'evidence': '1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6',
                'evidence_date': '2019-03-11 10:57:45',
                'evidence_file': '1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad',
                'evidence_file_date': '2019-03-11 10:57:45',
            },
            {
                'project_name': 'group1',
                'event_id': '418900980',
                'accessibility': 'Repositorio',
                'affected_components': 'affected_components_test',
                'action_after_blocking': 'EXECUTE_OTHER_PROJECT_SAME_CLIENT',
                'action_before_blocking': 'TEST_OTHER_PART_TOE',
                'analyst': 'unittest@fluidattacks.com',
                'client': 'Fluid',
                'client_project': 'group1',
                'closer': 'unittest',
                'closing_date': '2018-06-27 14:40:05',
                'context': 'FLUID',
                'detail': 'Integrates unit test2',
                'historic_state': [
                    {
                        'analyst': 'unittest@fluidattacks.com',
                        'date': '2018-06-27 07:00:00',
                        'state': 'OPEN',
                    },
                    {
                        'analyst': 'unittest@fluidattacks.com',
                        'date': '2018-06-27 14:40:05',
                        'state': 'CREATED',
                    },
                ],
                'event_type': 'OTHER',
                'hours_before_blocking': '1',
                'subscription': 'ONESHOT',
                'evidence': '1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6',
                'evidence_date': '2019-03-11 10:57:45',
                'evidence_file': '1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad',
                'evidence_file_date': '2019-03-11 10:57:45',
            },
            {
                'project_name': 'group1',
                'event_id': '418900995',
                'accessibility': 'Repositorio',
                'affected_components': 'affected_components_test',
                'action_after_blocking': 'EXECUTE_OTHER_PROJECT_SAME_CLIENT',
                'action_before_blocking': 'TEST_OTHER_PART_TOE',
                'analyst': 'unittest@fluidattacks.com',
                'client': 'Fluid',
                'client_project': 'group1',
                'closer': 'unittest',
                'closing_date': '2018-06-27 14:40:05',
                'context': 'FLUID',
                'detail': 'Integrates unit test2',
                'historic_state': [
                    {
                        'analyst': 'unittest@fluidattacks.com',
                        'date': '2018-06-27 07:00:00',
                        'state': 'OPEN',
                    },
                    {
                        'analyst': 'unittest@fluidattacks.com',
                        'date': '2018-06-27 14:40:05',
                        'state': 'CREATED',
                    },
                ],
                'event_type': 'OTHER',
                'hours_before_blocking': '1',
                'subscription': 'ONESHOT',
                'evidence': '1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6',
                'evidence_date': '2019-03-11 10:57:45',
                'evidence_file': '1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad',
                'evidence_file_date': '2019-03-11 10:57:45',
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
                'level': 'user',
                'subject': 'closer@gmail.com',
                'object': 'self',
                'role': 'user',
            },
            {
                'level': 'group',
                'subject': 'closer@gmail.com',
                'object': 'group1',
                'role': 'closer',
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
