# pylint: disable=unused-argument

import os
from toolbox import (
    resources,
)
from typing import (
    Any,
)

# Constants
SUBS: str = "continuoustest"
SUBS_BAD: str = "not-existing-group"
SUCCESS: int = 0
FAILURE: int = 1
FINDING: str = "720412598"
EMAIL: str = "dalvarez@fluidattacks.com"


def test_toolbox_get_fingerprint(relocate: Any) -> None:
    """Run required toolbox commands."""
    assert resources.get_fingerprint(SUBS)
    assert not resources.get_fingerprint(SUBS_BAD)
    os.mkdir(os.path.join("groups", "testfinger"))
    assert not resources.get_fingerprint("testfinger")
    os.mkdir(os.path.join("groups/testfinger", "fusion"))
    assert not resources.get_fingerprint("testfinger")
    os.rmdir(os.path.join("groups/testfinger", "fusion"))
    os.rmdir(os.path.join("groups", "testfinger"))


def test_format_repo_problem(relocate: Any) -> None:
    """Regression test to format problems."""
    expected_repo_problem = {
        "repo": "repo_test",
        "problem": "test",
    }
    expected_repo_problem_bad = {
        "nickname": "repo_test",
        "problem": "test",
    }
    repo_problem = resources.format_repo_problem("repo_test", "master", "test")
    assert repo_problem == expected_repo_problem
    assert repo_problem != expected_repo_problem_bad
