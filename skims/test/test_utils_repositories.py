# Standard libraries
from functools import (
    partial,
)
import textwrap

# Third party libraries
import git
import pytest

# Local libraries
from utils.repositories import (
    DEFAULT_COMMIT,
    RebaseResult,
    get_diff,
    get_repo,
    get_repo_head_hash,
    rebase,
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
    with pytest.raises(git.GitError):
        assert get_diff(repo, rev_a="xxxx", rev_b="HEAD")

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


@pytest.mark.skims_test_group("unittesting")
def test_rebase() -> None:
    repo = get_repo(".")

    # https://gitlab.com/fluidattacks/product/-/commit/2aa90d5
    rev = "2aa90d52561c24ea3cee4e5e1abb8686f7655068"
    rebase_ = partial(rebase, repo, rev_a=f"{rev}~1", rev_b=rev)

    # This is the original file
    path = "makes/applications/skims/process-group/src/get_config.py"

    # Line 69 becomes 66
    assert rebase_(path=path, line=69) == RebaseResult(
        path=path, line=66, rev=rev
    )

    # Line 64 becomes 64
    assert rebase_(path=path, line=64) == RebaseResult(
        path=path, line=64, rev=rev
    )

    # Line [65, 68] were modified, so no rebase is possible
    for line in range(65, 69):
        assert rebase_(path=path, line=line) is None

    assert rebase(
        repo, path=path, line=65, rev_a=f"{rev}~10", rev_b="HEAD"
    ) == RebaseResult(
        # Up to the parent of 2aa90d52561c24ea3cee4e5e1abb8686f7655068
        # Which is the commit before the line was modified
        path=path,
        line=65,
        rev="8deeafc8296e743ea31aef3fbc94aafdcfea509c",
    )

    # The file was deleted, we cannot rebase
    # https://gitlab.com/fluidattacks/product/-/commit/ca8916e
    rev = "ca8916ee4c68596ba7c6edaf70d08b585b775f77"
    path = "airs/content/pages/products/rules/findings/hygiene/037/index.adoc"
    assert None is rebase(repo, path=path, line=1, rev_a=f"{rev}~1", rev_b=rev)

    # The file was renamed, path is changed, line not
    # https://gitlab.com/fluidattacks/product/-/commit/72a8ce1
    rev = "72a8ce1ddaf4fb61579c35292340da6caf63af23"
    path_a = "skims/skims/core/entrypoint.py"
    path_b = "skims/skims/core/scan.py"
    assert RebaseResult(path=path_b, line=10, rev=rev) == rebase(
        repo, path=path_a, line=10, rev_a=f"{rev}~1", rev_b=rev
    )
