# Standard library
from typing import Tuple

# Local imports
from toolbox.helper import integrates
from toolbox.constants import SAST, DAST

# Constants
SUBS: str = 'continuoustest'
FINDING: str = '975673437'
FINDING_BAD: str = '000000000'
FINDING_DRAFT: str = '878487977'
FINDING_ACCEPTED: str = '720412598'
FINDING_OPEN: str = FINDING_ACCEPTED
FINDING_CLOSED: str = FINDING


def test_helper_does_finding_exist():
    """Test helper.does_finding_exist."""
    assert integrates.does_finding_exist(FINDING)
    assert not integrates.does_finding_exist(FINDING_BAD)


def test_helper_is_finding_accepted():
    """Test helper.is_finding_accepted."""
    assert not integrates.is_finding_accepted(FINDING)
    assert integrates.is_finding_accepted(FINDING_ACCEPTED)


def test_helper_is_finding_released():
    """Test helper.is_finding_released."""
    assert integrates.is_finding_released(FINDING)
    assert integrates.is_finding_released(FINDING_ACCEPTED)
    assert not integrates.is_finding_released(FINDING_DRAFT)


def test_helper_is_finding_open():
    """Test helper.is_finding_open."""
    assert integrates.is_finding_open(FINDING_OPEN, SAST)
    assert integrates.is_finding_open(FINDING_OPEN, DAST)
    assert not integrates.is_finding_open(FINDING_CLOSED, SAST)
    assert not integrates.is_finding_open(FINDING_CLOSED, DAST)


def test_helper_get_finding_title():
    """Test helper.get_finding_title."""
    finding_title: str = \
        'FIN.S.0002. PLEASE DO NOT EDIT THIS FINDING I USE THIS IN UNIT TESTS'
    assert integrates.get_finding_title(FINDING) == finding_title


def test_helper_get_finding_cvss_score():
    """Test helper.get_finding_cvss_score."""
    assert integrates.get_finding_cvss_score(FINDING) == 5.3


def test_helper_get_finding_description():
    """Test helper.get_finding_description."""
    assert integrates.get_finding_description(FINDING) == '.'


def test_helper_get_finding_threat():
    """Test helper.get_finding_threat."""
    assert integrates.get_finding_threat(FINDING) == '.'


def test_helper_get_finding_attack_vector():
    """Test helper.get_finding_attack_vector."""
    assert integrates.get_finding_attack_vector(FINDING) == '.'


def test_helper_get_finding_recommendation():
    """Test helper.get_finding_recommendation."""
    assert integrates.get_finding_recommendation(FINDING) == '.'


def test_helper_get_project_findings():
    """Test helper.get_project_findings."""
    finding_id__title = integrates.get_project_findings(SUBS)
    finding_ids = tuple(map(lambda x: x[0], finding_id__title))
    assert FINDING in finding_ids
    assert FINDING_ACCEPTED in finding_ids
    assert FINDING_DRAFT not in finding_ids


def test_helper_get_finding_type():
    """Test helper.get_finding_type."""
    assert integrates.get_finding_type(FINDING) == (True, True)
    assert integrates.get_finding_type(FINDING_ACCEPTED) == (True, True)


def test_helper_delete_pending_vulns():
    """Test helper.delete_pending_vulns."""
    assert integrates.delete_pending_vulns(FINDING)


def test_get_finding_repos():
    """Test helper.get_finding_repos."""
    result = integrates.get_finding_repos(FINDING)
    expected = ('Test', 'NoRepo')
    result, expected = tuple(sorted(result)), tuple(sorted(expected))
    assert result == expected
