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
@pytest.mark.resolver_test_group('download_file')
@pytest.fixture(autouse=True, scope='session')
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
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
                'files': [
                    {
                        'description': 'Test',
                        'file_name': 'test.zip',
                        'upload_date': '2019-03-01 15:21',
                        'uploader': 'unittest@fluidattacks.com',
                    },
                    {
                        'description': 'Test',
                        'file_name': 'shell.exe',
                        'upload_date': '2019-04-24 14:56',
                        'uploader': 'unittest@fluidattacks.com',
                    },
                    {
                        'description': 'Test',
                        'file_name': 'shell2.exe',
                        'upload_date': '2019-04-24 14:59',
                        'uploader': 'unittest@fluidattacks.com',
                    },
                    {
                        'description': 'Test',
                        'file_name': 'asdasd.py',
                        'upload_date': '2019-08-06 14:28',
                        'uploader': 'unittest@fluidattacks.com',
                    },
                    
                ],
            },
        ],
    }
    return await db.populate({**generic_data['db_data'], **data})
