import pathspec
from toolbox.drills import (
    pull_repos,
)
from toolbox.drills.pull_repos import (
    match_file,
)

EXISTING_REPO: str = "continuoustest"
EXISTING_REPO_NO_PERMISSIONS: str = "daimon"
NON_EXISTING_REPO: str = "sodjfoisajfdoiasjfdoia"
LOCAL_PATH = "continuoustest"


def test_drills_pull_repos() -> None:
    assert pull_repos.main(EXISTING_REPO, "*")
    assert not pull_repos.main(NON_EXISTING_REPO, "*")


def test_get_repo_from_url() -> None:
    for url, repo in (
        (
            "ssh://git@gitlab.com:fluidattacks/product.git",
            "product",
        ),
        (
            (
                "ssh://git@vs-ssh.visualstudio.com:v3/grupo/"
                "something Tecnología/Test"
            ),
            "Test",
        ),
        (
            (
                "ssh://git@vs-ssh.visualstudio.com:v3/grupo/"
                "something+Tecnolog%C3%ADa/Test+test"
            ),
            "Test test",
        ),
    ):
        assert pull_repos.get_repo_from_url(url) == repo


def test_match_file() -> None:
    patterns = ["!/integrates/"]
    spec_ignore = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    assert match_file(spec_ignore.patterns, "build/default.nix")
    assert match_file(spec_ignore.patterns, ".gitlab-ci.yml")
    assert not match_file(
        spec_ignore.patterns, "integrates/front/package.json"
    )

    patterns = ["aaa/*", "!aaa/ccc", "!aaa/ccc/*", "node_modules/"]
    spec_ignore = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    assert not match_file(spec_ignore.patterns, "aaa/ccc/aaa")
    assert match_file(spec_ignore.patterns, "aaa/ccc/aaa/bbb")
    assert not match_file(spec_ignore.patterns, "aaa/ccc")
    assert match_file(spec_ignore.patterns, "aaa/bbb")
    assert match_file(spec_ignore.patterns, "dddd")

    patterns = ["test/**/async/*", "make/install/**", "**/component/*.tsx"]
    spec_ignore = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    assert match_file(spec_ignore.patterns, "test/create/async/load.js")
    assert not match_file(spec_ignore.patterns, "test/create/block/load.js")
    assert not match_file(spec_ignore.patterns, "test/create/main.js")
    assert not match_file(spec_ignore.patterns, "dist/create/main.js")
    assert match_file(spec_ignore.patterns, "make/install/bundle/main.java")
    assert match_file(spec_ignore.patterns, "make/install/static/.icon")
    assert match_file(spec_ignore.patterns, "user/component/list.tsx")
    assert not match_file(spec_ignore.patterns, "client/component/list.ts")
