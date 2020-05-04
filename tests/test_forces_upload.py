# Local imports
from toolbox.forces.upload import (
    _get_exploits_for_finding,
    _get_exploits_bundles,
    from_repo_to_integrates,
)

# Constants
GROUP: str = 'continuoustest'
GROUP_BAD: str = 'does-not-exist'
FINDING: str = '720412598'
FINDING_BAD: str = 'does-not-exist'


def test__get_exploits_for_finding_1(relocate):
    result = _get_exploits_for_finding(GROUP, FINDING)

    assert sorted(result.keys()) == [
        'groups/continuoustest/forces/dynamic/exploits/720412598.exp',
        'groups/continuoustest/forces/static/exploits/720412598.exp',
    ]
    assert all(len(result[exp]) > 0 for exp in result)


def test__get_exploits_for_finding_2(relocate):
    assert _get_exploits_for_finding(GROUP, FINDING_BAD) == {}


def test__get_exploits_bundles(relocate):
    result = _get_exploits_bundles(GROUP)

    assert sorted(result.keys()) == [
        '508273958',
        '710340580',
        '720412598',
        '975673437',
    ]
    assert all(len(result[exp]) > 0 for exp in result)
