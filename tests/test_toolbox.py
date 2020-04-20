# Standard library
import os
import sys

# Third parties imports
import pytest

# Local libraries
from toolbox import (
    forces,
    helper,
    toolbox,
)

# Constants
SUBS: str = 'continuoustest'
SUBS_BAD: str = 'not-existing-subscription'
SUCCESS: int = 0
FAILURE: int = 1
FINDING: str = '720412598'


def test_toolbox_statefull_functions(relocate_to_cloned_repo):
    """Test functions that modify files."""
    # This tests need to be run in a pristine environment
    assert not os.system('git reset --hard HEAD')

    try:
        # Secrets management
        assert toolbox.init_secrets(SUBS)
        assert toolbox.encrypt_secrets(SUBS)
        assert toolbox.decrypt_secrets(SUBS)

        # Deployment phase
        assert toolbox.fill_with_mocks(subs_glob=SUBS, create_files=True)
        assert toolbox.generate_exploits(subs_glob=SUBS)
    finally:
        os.system('git reset --hard HEAD')


def test_toolbox_reporting_cycle(relocate):
    """Test reporting cycle."""
    assert forces.sync.are_exploits_synced(SUBS, exp_name=None)
    assert toolbox.run_static_exploits(SUBS, exp_name=None)
    assert toolbox.run_dynamic_exploits(SUBS, exp_name=None)
    assert toolbox.get_vulnerabilities_yaml(SUBS)
    assert toolbox.get_exps_fragments(SUBS, exp_name=None)
    assert toolbox.report_vulnerabilities(SUBS, vulns_name=None)

    # remove the reported vulnerabilities
    assert helper.integrates.delete_pending_vulns(FINDING)


def test_toolbox_get_subscription_from_commit_msg(relocate):
    """Test toolbox.get_subscription_from_commit_msg."""
    toolbox.get_subscription_from_commit_msg()


def test_toolbox_does_subs_exist(relocate):
    """Test toolbox.does_subs_exist."""
    assert toolbox.does_subs_exist(SUBS)
    assert not toolbox.does_subs_exist(SUBS_BAD)


def test_toolbox_get_static_dictionary(relocate):
    """Test toolbox.get_static_dictionary."""
    assert toolbox.get_static_dictionary(SUBS)


def test_toolbox_has_break_build(relocate):
    """Run required toolbox commands."""
    assert toolbox.has_break_build(SUBS)
    assert not toolbox.has_break_build(SUBS_BAD)
