# Standard library
from typing import (
    Set,
)

# Third party libraries
import pytest

# Local libraries
from backend import authz

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_group_level_enforcer():
    model = authz.GROUP_LEVEL_ROLES
    subject = 'test@tests.com'
    group = 'test'

    for role in model:
        authz.revoke_user_level_role(subject)
        authz.revoke_group_level_role(subject, group)
        authz.grant_group_level_role(subject, group, role)
        enforcer = authz.get_group_level_enforcer(subject)

        for action in model[role]['actions']:
            assert await enforcer(subject, group, action), \
                f'{role} should be able to do {action}'

        for other_role in model:
            for action in model[other_role]['actions'] - model[role]['actions']:
                assert not await enforcer(subject, group, action), \
                    f'{role} should not be able to do {action}'


@pytest.mark.parametrize(
    ['request_role', 'request_subscribed_projects', 'request_object', 'result'],
    [
        # People not member of a project
        ('admin', {}, 'testgroup', True),
        ('nonadmin', {}, 'testgroup', False),

        # People members of 'testgroup'
        ('admin', {'testgroup'}, 'testgroup', True),
        ('admin', {'testgroup'}, 'TESTGROUP', True),
        ('admin', {'testgroup'}, 'othertestgroup', True),
        ('admin', {'testgroup'}, 'OTHERTESTGROUP', True),
        ('nonadmin', {'testgroup'}, 'testgroup', True),
        ('nonadmin', {'testgroup'}, 'TESTGROUP', True),
        ('nonadmin', {'testgroup'}, 'othertestgroup', False),
        ('nonadmin', {'testgroup'}, 'OTHERTESTGROUP', False),
    ]
)
async def test_group_access_enforcer(
    request_role: str,
    request_subscribed_projects: Set[str],
    request_object: str,
    result: bool,
):
    enforcer = authz.get_group_access_enforcer()

    request_data: dict = {
        'role': request_role,
        'subscribed_projects': request_subscribed_projects,
    }

    assert await enforcer(request_data, request_object) == result, (
        f'request with params: {request_data}'
        f', to object: {request_object}'
        f', should return: {result}'
    )


async def test_user_level_enforcer():
    model = authz.USER_LEVEL_ROLES
    subject = 'test@tests.com'
    object_ = 'self'

    for role in model:
        authz.revoke_user_level_role(subject)
        authz.grant_user_level_role(subject, role)
        enforcer = authz.get_user_level_enforcer(subject)

        for action in model[role]['actions']:
            assert await enforcer(subject, object_, action), \
                f'{role} should be able to do {action}'

        for other_role in model:
            for action in model[other_role]['actions'] - model[role]['actions']:
                assert not await enforcer(subject, object_, action), \
                    f'{role} should not be able to do {action}'


async def test_group_service_attributes_enforcer():
    # All attributes must be tested for this test to succeed
    # This prevents someone to add a new attribute without testing it

    attributes_remaining_to_test: Set[str] = {
        (group, attr)
        for group in ('unittesting', 'oneshottest', 'non_existing')
        for attrs in authz.SERVICE_ATTRIBUTES.values()
        for attr in set(attrs).union({'non_existing_attribute'})
    }

    for group, attribute, result in [
        ('unittesting', 'is_fluidattacks_customer', True),
        ('unittesting', 'must_only_have_fluidattacks_hackers', True),
        ('unittesting', 'non_existing_attribute', False),

        ('oneshottest', 'is_fluidattacks_customer', True),
        ('oneshottest', 'must_only_have_fluidattacks_hackers', True),
        ('oneshottest', 'non_existing_attribute', False),

        ('non_existing', 'is_fluidattacks_customer', False),
        ('non_existing', 'must_only_have_fluidattacks_hackers', False),
        ('non_existing', 'non_existing_attribute', False),
    ]:
        enforcer = authz.get_group_service_attributes_enforcer(group)

        assert await enforcer(group, attribute) == result, \
            f'{group} attribute: {attribute}, should have value {result}'

        attributes_remaining_to_test.remove((group, attribute))

    assert not attributes_remaining_to_test, (
        f'Please add tests for the following pairs of (group, attribute)'
        f': {attributes_remaining_to_test}'
    )
