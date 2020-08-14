# Standard library

# Third party libraries
import pytest

# Local libraries
from backend import authz

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ['parameter', 'expected'],
    [
        (authz.GROUP_LEVEL_ROLES, [
            'admin',
            'analyst',
            'closer',
            'customer',
            'customeradmin',
            'executive',
            'group_manager',
            'resourcer',
            'reviewer',
            'service_forces'
        ]),
        (authz.USER_LEVEL_ROLES, [
            'admin',
            'analyst',
            'customer',
            'internal_manager'
        ]),
        (authz.SERVICE_ATTRIBUTES, [
            'drills_black',
            'drills_white',
            'forces',
            'integrates',
        ])
    ],
)
def test_model_integrity_keys_1(parameter, expected):
    assert sorted(parameter.keys()) == expected


@pytest.mark.parametrize(
    ['parameter'],
    [
        [authz.GROUP_LEVEL_ROLES],
        [authz.USER_LEVEL_ROLES],
    ],
)
def test_model_integrity_keys_2(parameter):
    for value in parameter.values():
        assert sorted(value.keys()) == ['actions', 'tags']
