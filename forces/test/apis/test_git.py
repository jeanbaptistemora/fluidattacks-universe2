# Third party libraries
import pytest
from git import Repo

# Local libraries
from forces.apis.git import get_repository_metadata


@pytest.mark.asyncio  # type: ignore
def test_get_repository_metadata_test() -> None:
    result = get_repository_metadata(repo_path='../')
    assert result['git_repo'] == 'integrates'
    assert 'integrates.git' in result['git_origin']
    assert result['git_branch'] != 'master'
