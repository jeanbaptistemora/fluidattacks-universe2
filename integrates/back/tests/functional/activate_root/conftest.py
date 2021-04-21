# Standard
import pytest
from typing import Any, Dict

# Local
from back.tests import db
from dynamodb.types import (
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
    IPRootItem,
    IPRootMetadata,
    IPRootState,
    URLRootItem,
    URLRootMetadata,
    URLRootState
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('activate_root')
@pytest.fixture(autouse=True, scope='session')
async def populate(generic_data: Dict[str, Any]) -> bool:
    test_email = 'admin@gmail.com'
    test_group = 'group1'
    test_date = '2020-11-19T13:37:10+00:00'
    test_status = 'INACTIVE'
    data: Dict[str, Any] = {
        'roots': (
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date=test_date,
                    reason='root creation',
                    status='UNKNOWN'
                ),
                group_name=test_group,
                id='63298a73-9dff-46cf-b42d-9b2f01a56690',
                metadata=GitRootMetadata(
                    branch='master',
                    type='Git',
                    url='https://gitlab.com/fluidattacks/product'
                ),
                state=GitRootState(
                    environment_urls=['https://test.com'],
                    environment='production',
                    gitignore=['bower_components/*', 'node_modules/*'],
                    includes_health_check=True,
                    modified_by=test_email,
                    modified_date=test_date,
                    new_repo=None,
                    nickname='',
                    reason=None,
                    status=test_status
                )
            ),
            IPRootItem(
                group_name=test_group,
                id='83cadbdc-23f3-463a-9421-f50f8d0cb1e5',
                metadata=IPRootMetadata(
                    address='192.168.1.1',
                    port='8080',
                    type='IP'
                ),
                state=IPRootState(
                    modified_by=test_email,
                    modified_date=test_date,
                    new_repo=None,
                    reason=None,
                    status=test_status
                )
            ),
            URLRootItem(
                group_name=test_group,
                id='eee8b331-98b9-4e32-a3c7-ec22bd244ae8',
                metadata=URLRootMetadata(
                    host='app.fluidattacks.com',
                    path='/',
                    port='8080',
                    protocol='HTTPS',
                    type='URL'
                ),
                state=URLRootState(
                    modified_by=test_email,
                    modified_date=test_date,
                    new_repo=None,
                    reason=None,
                    status=test_status
                )
            )
        )
    }

    return await db.populate({**generic_data['db_data'], **data})
