# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from os.path import (
    join,
)
import pytest
import textwrap
from utils.repositories import (
    DEFAULT_COMMIT,
    get_diff,
    get_repo,
    get_repo_head_hash,
)


@pytest.mark.skims_test_group("unittesting")
def test_get_repo_head_hash() -> None:
    base = "../universe"
    head = get_repo_head_hash(base)
    assert head != DEFAULT_COMMIT

    for path, commit_hash in (
        # Not a repository
        ("/", DEFAULT_COMMIT),
        # Not exist
        ("/path-not-exists", DEFAULT_COMMIT),
        # Inside a repository, file
        ("skims/test/data/config/lib_path.yaml", head),
        # Inside a repository, directory
        ("skims/test/data/parse_hcl2", head),
        # Inside a repsitory, not exists
        ("skims/test/path-not-exists", DEFAULT_COMMIT),
    ):
        assert get_repo_head_hash(join(base, path)) == commit_hash, path


@pytest.mark.skims_test_group("unittesting")
def test_get_diff() -> None:
    repo = get_repo("../universe")

    # Nice format
    path: str = "makes/packages/skims/config-runtime/default.nix"
    # Wrong format
    assert get_diff(repo, rev_a="xxxx", rev_b="HEAD") is None

    assert (
        str(
            get_diff(
                repo,
                # integrates\feat(front): #4443.22 daily digest modal
                rev_a="4db24690eb0381bb4645a2617eda2fd26d511e74",
                # skims\feat(build): #4551.11 add unidiff library
                rev_b="992a60f0eead2898726d02c89077afecdce68e61",
            ),
        )
        == textwrap.dedent(
            f"""
            diff --git a/{path} b/{path}
            index c59a5db2f0..082551229a 100644
            --- a/{path}
            +++ b/{path}
            @@ -29,0 +30,1 @@ makeTemplate {{
            +      nixpkgs.python38Packages.unidiff
            """,
        )[1:-1]
    )
