from functools import (
    partial,
)
import git
import pytest
import textwrap
from utils.repositories import (
    DEFAULT_COMMIT,
    get_diff,
    get_repo,
    get_repo_head_hash,
    rebase,
    RebaseResult,
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
                rev_a="4db24690eb0381bb4645a2617eda2fd26d511e74",
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


@pytest.mark.skims_test_group("unittesting")
def test_rebase() -> None:
    repo = get_repo(".")

    rev = "1a5763f0ea8aa867ba459c629c42919243a89521"
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
        # Up to the parent of 1a5763f0ea8aa867ba459c629c42919243a89521
        # Which is the commit before the line was modified
        path=path,
        line=65,
        rev="5d7f7915544aa5c9fba828331ed9f200f5ac5ed1",
    )

    # The file was deleted, we cannot rebase
    rev = "e96763322ba55cc62684303cf1589870220825fa"
    path = "airs/content/pages/products/rules/findings/hygiene/037/index.adoc"
    assert None is rebase(repo, path=path, line=1, rev_a=f"{rev}~1", rev_b=rev)

    # The file was renamed, path is changed, line not
    rev = "2d1a923747b0f26f41c3f23e104598fefd4de6eb"
    path_a = "skims/skims/core/entrypoint.py"
    path_b = "skims/skims/core/scan.py"
    assert RebaseResult(path=path_b, line=10, rev=rev) == rebase(
        repo, path=path_a, line=10, rev_a=f"{rev}~1", rev_b=rev
    )
