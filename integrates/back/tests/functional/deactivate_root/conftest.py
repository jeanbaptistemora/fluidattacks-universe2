# Standard
import pytest
from typing import Any, Dict

# Local
from back.tests import db
from dynamodb.types import (
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('deactivate_root')
@pytest.fixture(autouse=True, scope='session')
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        'roots': (
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date='2020-11-19T13:37:10+00:00',
                    reason='root creation',
                    status='UNKNOWN'
                ),
                group_name='group1',
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
                    modified_by='admin@gmail.com',
                    modified_date='2020-11-19T13:37:10+00:00',
                    new_repo=None,
                    nickname='nickname',
                    reason=None,
                    status='ACTIVE'
                )
            ),
        )
    }

    return await db.populate({**generic_data, **data})
