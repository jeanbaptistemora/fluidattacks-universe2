import pytest
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


@pytest.mark.skip(reason="test should not depend on prod integrates")
def test_get_groups_with_forces() -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    groups = get_groups_with_forces()
    assert "continuoustest" in groups


@pytest.mark.skip(reason="test should not depend on prod integrates")
def test_has_forces() -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    assert has_forces("continuoustest")
    try:
        assert has_forces("undefined")
    except IntegratesError:
        assert True
    else:
        assert False


@pytest.mark.skip(reason="test should not depend on prod integrates")
def test_get_repos() -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    repos = get_group_repos("continuoustest")
    assert not repos
    assert not get_group_repos("undefined")


@pytest.mark.skip(reason="test should not depend on prod integrates")
def test_get_group_language() -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    assert get_group_language("continuoustest") == "EN"
    try:
        assert get_group_language("undefined")
    except IntegratesError:
        assert True
    else:
        assert False


@pytest.mark.skip(reason="test should not depend on prod integrates")
def test_has_drills() -> None:
    # TODO: refactor this test to point to a test group in a dev environment
    assert has_squad("continuoustest")
    try:
        assert has_squad("undefined")
    except IntegratesError:
        assert True
    else:
        assert False
