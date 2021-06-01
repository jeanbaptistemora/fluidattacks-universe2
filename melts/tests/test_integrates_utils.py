from toolbox.api.exceptions import (
    IntegratesError,
)
from toolbox.utils.integrates import (
    get_group_language,
    get_project_repos,
    get_projects_with_forces,
    has_drills,
    has_forces,
)


def test_get_projects_with_forces() -> None:
    projects = get_projects_with_forces()
    assert "continuoustest" in projects


def test_has_forces() -> None:
    assert has_forces("continuoustest")
    try:
        assert has_forces("undefined")
    except IntegratesError:
        assert True
    else:
        assert False


def test_get_repos() -> None:
    repos = get_project_repos("continuoustest")
    assert not repos
    assert not get_project_repos("undefined")


def test_get_group_language() -> None:
    assert get_group_language("continuoustest") == "EN"
    try:
        assert get_group_language("undefined")
    except IntegratesError:
        assert True
    else:
        assert False


def test_has_drills() -> None:
    assert has_drills("continuoustest")
    try:
        assert has_drills("undefined")
    except IntegratesError:
        assert True
    else:
        assert False
