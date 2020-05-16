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
    user_level_role = authz.get_user_level_role(email)

    assert await authz.get_user_level_actions(email) \
        == authz.USER_LEVEL_ROLES.get(user_level_role, {}).get('actions')


@pytest.mark.parametrize(
    ['email', 'group'],
    [
        ['continuoushacking@gmail.com', 'unittesting'],
        ['continuoushacking@gmail.com', 'oneshottest'],
        ['integratesuser@gmail.com', 'unittesting'],
        ['integratesuser@gmail.com', 'oneshottest'],
    ]
)
async def test_get_group_level_actions(email, group):
    group_level_role = authz.get_group_level_role(email, group)

    assert await authz.get_group_level_actions(email, group) \
        == authz.GROUP_LEVEL_ROLES.get(group_level_role, {}).get('actions')
