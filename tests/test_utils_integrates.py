# Standard library
from typing import Tuple

# Local imports
from toolbox.utils.integrates import (
    delete_pending_vulns,
    does_finding_exist,
    get_finding_attack_vector,
    get_finding_cvss_score,
    get_finding_description,
    get_finding_dynamic_states,
    get_finding_recommendation,
    get_finding_repos,
    get_finding_static_states,
    get_finding_static_repos_states,
    get_finding_static_repos_vulns,
    get_finding_threat,
    get_finding_title,
    get_finding_type,
    get_project_findings,
    is_finding_accepted,
    is_finding_open,
    is_finding_released,
)
from toolbox.constants import SAST, DAST

# Constants
SUBS: str = 'continuoustest'
FINDING: str = '975673437'
FINDING_BAD: str = '000000000'
FINDING_DRAFT: str = '878487977'
FINDING_ACCEPTED: str = '720412598'
FINDING_OPEN: str = FINDING_ACCEPTED
FINDING_CLOSED: str = FINDING


def test_does_finding_exist():
    """Test utils.does_finding_exist."""
    assert does_finding_exist(FINDING)
    assert not does_finding_exist(FINDING_BAD)


def test_is_finding_accepted():
    """Test utils.is_finding_accepted."""
    assert not is_finding_accepted(FINDING)
    assert is_finding_accepted(FINDING_ACCEPTED)


def test_is_finding_released():
    """Test utils.is_finding_released."""
    assert is_finding_released(FINDING)
    assert is_finding_released(FINDING_ACCEPTED)
    assert not is_finding_released(FINDING_DRAFT)


def test_is_finding_open():
    """Test utils.is_finding_open."""
    assert is_finding_open(FINDING_OPEN, SAST)
    assert is_finding_open(FINDING_OPEN, DAST)
    assert not is_finding_open(FINDING_CLOSED, SAST)
    assert not is_finding_open(FINDING_CLOSED, DAST)


def test_get_finding_title():
    """Test utils.get_finding_title."""
    finding_title: str = \
        'FIN.S.0002. PLEASE DO NOT EDIT THIS FINDING I USE THIS IN UNIT TESTS'
    assert get_finding_title(FINDING) == finding_title


def test_get_finding_cvss_score():
    """Test utils.get_finding_cvss_score."""
    assert get_finding_cvss_score(FINDING) == 5.3


def test_get_finding_description():
    """Test utils.get_finding_description."""
    assert get_finding_description(FINDING) == '.'


def test_get_finding_static_states():
    assert get_finding_static_states(FINDING_OPEN) == (
        ('Test', '2019-09-23 16:24:01.619957', '1', True),
        ('continuous', '2019-09-23 16:24:01.619957', '1', True),
    )


def test_get_finding_dynamic_states_open():
    assert get_finding_dynamic_states(FINDING_OPEN) == (
        ('https://aa.com', 'f', True),
        ('192.168.1.102', '9999', False),
        ('192.168.1.104', '2222', False),
        ('https://bb.com', 'f', True),
        ('192.168.1.103', '3333', True),
        ('192.168.1.102', '5555', False),
        ('https://dd.com', 'phonee', False),
        ('https://example.com', 'phone', True),
        ('https://cc.com', 'phonee', True),
        ('192.168.1.102', '4444', False),
    )


def test_get_finding_static_repos_states_closed():
    result = get_finding_static_repos_states(FINDING_CLOSED)
    expected = {
        'NoRepo': False,
        'Test': False,
    }

    assert sorted(result.keys()) == sorted(expected.keys())

    for repo in result:
        assert result[repo] == expected[repo], repo


def test_get_finding_static_repos_states_open():
    result = get_finding_static_repos_states(FINDING_OPEN)
    expected = {
        'Test': True,
        'continuous': True,
    }

    assert sorted(result.keys()) == sorted(expected.keys())

    for repo in result:
        assert result[repo] == expected[repo], repo


def test_get_finding_static_repos_vulns_closed():
    result = get_finding_static_repos_vulns(FINDING_CLOSED)
    expected = {
        'NoRepo': {
            'open': 0,
            'closed': 1,
        },
        'Test': {
            'open': 0,
            'closed': 3,
        },
    }

    assert sorted(result.keys()) == sorted(expected.keys())

    for repo in result:
        assert result[repo] == expected[repo], repo


def test_get_finding_static_repos_vulns_open():
    result = get_finding_static_repos_vulns(FINDING_OPEN)
    expected = {
        'Test': {
            'open': 1,
            'closed': 0,
        },
        'continuous': {
            'open': 1,
            'closed': 0,
        },
    }

    assert sorted(result.keys()) == sorted(expected.keys())

    for repo in result:
        assert result[repo] == expected[repo], repo


def test_get_finding_threat():
    """Test utils.get_finding_threat."""
    assert get_finding_threat(FINDING) == '.'


def test_get_finding_attack_vector():
    """Test utils.get_finding_attack_vector."""
    assert get_finding_attack_vector(FINDING) == '.'


def test_get_finding_recommendation():
    """Test utils.get_finding_recommendation."""
    assert get_finding_recommendation(FINDING) == '.'


def test_get_project_findings():
    """Test utils.get_project_findings."""
    finding_id__title = get_project_findings(SUBS)
    finding_ids = tuple(map(lambda x: x[0], finding_id__title))
    assert FINDING in finding_ids
    assert FINDING_ACCEPTED in finding_ids
    assert FINDING_DRAFT not in finding_ids


def test_get_finding_type():
    """Test utils.get_finding_type."""
    assert get_finding_type(FINDING) == (True, True)
    assert get_finding_type(FINDING_ACCEPTED) == (True, True)


def test_delete_pending_vulns():
    """Test utils.delete_pending_vulns."""
    assert delete_pending_vulns(FINDING)


def test_get_finding_repos():
    """Test utils.get_finding_repos."""
    result = get_finding_repos(FINDING)
    expected = ('Test', 'NoRepo')
    result, expected = tuple(sorted(result)), tuple(sorted(expected))
    assert result == expected
