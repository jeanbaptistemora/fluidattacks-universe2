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
@pytest.mark.resolver_test_group('create_draft')
@pytest.fixture(autouse=True, scope='session')
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
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
            }
        ],
    }
    return await db.populate({**generic_data, **data})
