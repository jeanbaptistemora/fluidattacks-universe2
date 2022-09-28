# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from toolbox.api.exceptions import (
    IntegratesError,
)
from toolbox.utils.integrates import (
    get_group_language,
    get_group_repos,
    get_groups_with_forces,
    has_forces,
    has_squad,
)

# Constants
GROUP: str = "absecon"


def test_get_groups_with_forces() -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    groups = get_groups_with_forces()
    assert GROUP in groups


def test_has_forces() -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    assert has_forces(GROUP)
    try:
        assert has_forces("undefined")
    except IntegratesError:
        assert True
    else:
        assert False


def test_get_repos() -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    repos = get_group_repos(GROUP)
    assert not repos
    assert not get_group_repos("undefined")


def test_get_group_language() -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    assert get_group_language(GROUP) == "EN"
    try:
        assert get_group_language("undefined")
    except IntegratesError:
        assert True
    else:
        assert False


def test_has_drills() -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    assert has_squad(GROUP)
    try:
        assert has_squad("undefined")
    except IntegratesError:
        assert True
    else:
        assert False
