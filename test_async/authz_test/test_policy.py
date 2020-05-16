# Third party libraries
import pytest

# Local libraries
from backend.authz import (
    get_cached_group_service_attributes_policies,
    get_group_level_role,
    get_user_level_role,
    grant_group_level_role,
    grant_user_level_role,
    revoke_user_level_role,
    revoke_group_level_role,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_cached_group_service_attributes_policies():
    function = get_cached_group_service_attributes_policies

    assert sorted(function('not-exists... probably')) == [
    ]
    assert sorted(function('oneshottest')) == [
        ('oneshottest', 'drills_black'),
        ('oneshottest', 'integrates'),
    ]
    assert sorted(function('unittesting')) == [
        ('unittesting', 'drills_white'),
        ('unittesting', 'forces'),
        ('unittesting', 'integrates'),
    ]


async def test_get_group_level_role():
    assert get_group_level_role('continuoushacking@gmail.com', 'unittesting') == 'customeradmin'
    assert get_group_level_role('integratesanalyst@gmail.com', 'unittesting') == 'analyst'
    assert get_group_level_role('integratesuser@gmail.com', 'unittesting') == 'customeradmin'
    assert get_group_level_role('unittest@fluidattacks.com', 'any-group') == 'admin'
    assert not get_group_level_role('asdfasdfasdfasdf@gmail.com', 'unittesting')


async def test_get_user_level_role():
    assert get_user_level_role('continuoushacking@gmail.com') == 'customeradmin'
    assert get_user_level_role('integratesanalyst@gmail.com') == 'analyst'
    assert get_user_level_role('integratesuser@gmail.com') == 'customeradmin'
    assert get_user_level_role('unittest@fluidattacks.com') == 'admin'
    assert not get_user_level_role('asdfasdfasdfasdf@gmail.com')


async def test_grant_user_level_role():
    assert grant_user_level_role('..TEST@gmail.com', 'customer')
    assert get_user_level_role('..test@gmail.com') == 'customer'
    assert get_user_level_role('..tEst@gmail.com') == 'customer'

    assert grant_user_level_role('..TEST@gmail.com', 'admin')
    assert get_user_level_role('..test@gmail.com') == 'admin'
    assert get_group_level_role('..tEst@gmail.com', 'a-group') == 'admin'


async def test_grant_group_level_role():
    assert grant_group_level_role('..TEST2@gmail.com', 'group', 'customer')
    assert get_user_level_role('..test2@gmail.com') == 'customer'
    assert get_user_level_role('..tESt2@gmail.com') == 'customer'
    assert get_group_level_role('..test2@gmail.com', 'GROUP') == 'customer'
    assert not get_group_level_role('..test2@gmail.com', 'other-group')


async def test_revoke_group_level_role():
    assert grant_group_level_role('revoke_group_LEVEL_role@gmail.com', 'group', 'customer')
    assert grant_group_level_role('REVOKE_group_level_role@gmail.com', 'other-group', 'customer')

    assert get_group_level_role('revoke_group_level_ROLE@gmail.com', 'group') == 'customer'
    assert get_group_level_role('revoke_GROUP_level_role@gmail.com', 'other-group') == 'customer'
    assert not get_group_level_role('REVOKE_group_level_role@gmail.com', 'yet-other-group')

    assert revoke_group_level_role('revoke_GROUP_level_role@gmail.com', 'other-group')
    assert get_group_level_role('revoke_group_level_role@gmail.com', 'group') == 'customer'
    assert not get_group_level_role('revoke_group_level_role@gmail.com', 'other-group')
    assert not get_group_level_role('revoke_group_level_role@gmail.com', 'yet-other-group')

    assert revoke_group_level_role('revoke_GROUP_level_role@gmail.com', 'group')
    assert not get_group_level_role('revOke_group_level_role@gmail.com', 'group')
    assert not get_group_level_role('revoKe_group_level_role@gmail.com', 'other-group')
    assert not get_group_level_role('revokE_group_level_role@gmail.com', 'yet-other-group')


async def test_revoke_user_level_role():
    assert grant_user_level_role('revoke_user_LEVEL_role@gmail.com', 'customer')

    assert get_user_level_role('revoke_user_level_ROLE@gmail.com') == 'customer'
    assert not get_user_level_role('REVOKE_user_level_role@gmail.net')
    assert revoke_user_level_role('revoke_USER_LEVEL_ROLE@gmail.com')
    assert not get_user_level_role('revoke_user_level_ROLE@gmail.com')
