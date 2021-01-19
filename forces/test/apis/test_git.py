# Third party libraries
import pytest

# Local libraries
from forces.apis.git import get_repository_metadata


@pytest.mark.asyncio
def test_get_repository_metadata_test() -> None:
    result = get_repository_metadata(repo_path='.')
    assert result['git_repo'] == 'product'
    assert 'product.git' in result['git_origin']
    assert result['git_branch'] != 'master'
