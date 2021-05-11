# Third party libraries
import textwrap
import pytest

# Local libraries
from utils.repositories import (
    DEFAULT_COMMIT,
    get_diff,
    get_repo,
    get_repo_head_hash,
)


@pytest.mark.skims_test_group("unittesting")
def test_get_repo_head_hash() -> None:
    head = get_repo_head_hash(".")
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
        assert get_repo_head_hash(path) == commit_hash, path


@pytest.mark.skims_test_group("unittesting")
def test_get_diff() -> None:
    repo = get_repo(".")

    # Wrong format
    assert get_diff(repo, rev_a="xxxx", rev_b="HEAD") is None

    # Nice format
    path: str = "makes/packages/skims/config-runtime/default.nix"

    assert (
        str(
            get_diff(
                repo,
                rev_a="0d057c386a062bfcb79f4d62a1494354a17b86de",
                rev_b="53787d7d48ec256fd592f9b05bff59b53f83284c",
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
