# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import pathspec
from toolbox.drills import (
    pull_repos,
)
from toolbox.drills.pull_repos import (
    match_file,
)

EXISTING_REPO: str = "absecon"
NON_EXISTING_REPO: str = "sodjfoisajfdoiasjfdoia"
LOCAL_PATH = "continuoustest"


def test_drills_pull_repos() -> None:
    assert pull_repos.main(EXISTING_REPO)
    assert not pull_repos.main(NON_EXISTING_REPO)


def test_get_repo_from_url() -> None:
    for url, repo in (
        (
            "https://gitlab.com/fluidattacks/product",
            "product",
        ),
        (
            "https://github.com/WebGoat/WebGoat",
            "WebGoat",
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
