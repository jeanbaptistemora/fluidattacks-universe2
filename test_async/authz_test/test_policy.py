# Third party libraries
import pytest

# Local libraries
from backend import authz

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_cached_group_service_attributes_policies():
    function = authz.get_cached_group_service_attributes_policies

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
