# Third party libraries
import pytest

# Local libraries
from utils.repositories import (
    DEFAULT_COMMIT,
    get_repo_head_hash,
)


@pytest.mark.skims_test_group('unittesting')
def test_get_repo_head_hash() -> None:
    head = get_repo_head_hash('.')
    assert head != DEFAULT_COMMIT

    for path, commit_hash in (
        # Not a repository
        ('/', DEFAULT_COMMIT),
        # Not exist
        ('/path-not-exists', DEFAULT_COMMIT),
        # Inside a repository, file
        ('skims/test/data/config/lib_path.yaml', head),
        # Inside a repository, directory
        ('skims/test/data/parse_hcl2', head),
        # Inside a repsitory, not exists
        ('skims/test/path-not-exists', DEFAULT_COMMIT),
    ):
        assert get_repo_head_hash(path) == commit_hash, path
