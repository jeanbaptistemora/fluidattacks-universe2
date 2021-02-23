# Third party libraries
import pytest

# Local libraries
from forces.apis.git import (
    get_repository_metadata,
    check_remotes,
)
from forces.apis.integrates import set_api_token
from forces.utils.model import ForcesConfig


@pytest.mark.asyncio
def test_get_repository_metadata_test() -> None:
    result = get_repository_metadata(repo_path='.')
    assert result['git_repo'] == 'product'
    assert 'product.git' in result['git_origin']
    assert result['git_branch'] != 'master'


@pytest.mark.asyncio
async def test_check_remotes(test_token: str) -> None:
    set_api_token(test_token)
    config = ForcesConfig(group='herrin', repository_name='product')
    assert await check_remotes(config)

    bad_config = ForcesConfig(group='herrin', repository_name='products')
    assert not await check_remotes(bad_config)
