# Standard library
from typing import (
    Set,
)

# Third party libraries
import pytest

# Local libraries
from backend import authz
from backend.domain import (
    user as user_domain,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ['email'],
    [
        ['continuoushacking@gmail.com'],
        ['integratesuser@gmail.com'],
    ]
)
async def test_get_user_level_actions(email):
    user_level_role = await authz.get_user_level_role(email)

    assert await authz.get_user_level_actions(email) \
        == authz.USER_LEVEL_ROLES.get(user_level_role, {}).get('actions')


@pytest.mark.parametrize(
    ['email', 'group'],
    [
        ['continuoushacking@gmail.com', 'UnItTeStInG'],
        ['continuoushacking@gmail.com', 'unittesting'],
        ['continuoushacking@gmail.com', 'oneshottest'],
        ['integratesuser@gmail.com', 'unittesting'],
        ['integratesuser@gmail.com', 'oneshottest'],
    ]
)
async def test_get_group_level_actions(email, group):
    group_level_role = await authz.get_group_level_role(email, group)

    assert await authz.get_group_level_actions(email, group) \
        == authz.GROUP_LEVEL_ROLES.get(group_level_role, {}).get('actions')


@pytest.mark.parametrize(
    ['email', 'organization_id'],
    [
        ['org_testgroupmanager1@gmail.com', 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'],
    ]
)
async def test_get_organization_level_actions(email, organization_id):
    organization_level_role = await authz.get_organization_level_role(email, organization_id)

    assert await authz.get_organization_level_actions(email, organization_id) \
        == authz.ORGANIZATION_LEVEL_ROLES.get(organization_level_role, {}).get('actions')
