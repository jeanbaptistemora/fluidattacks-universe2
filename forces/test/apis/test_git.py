from forces.apis.git import (
    check_remotes,
    extract_repo_name,
    get_repo_name_from_vars,
    get_repository_metadata,
)
from forces.apis.integrates import (
    set_api_token,
)
from forces.utils.model import (
    ForcesConfig,
)
import os
import pytest


@pytest.mark.asyncio
def test_get_repository_metadata_test() -> None:
    result = get_repository_metadata(repo_path=".")
    assert result["git_repo"] == "product"
    assert "fluidattacks/product" in result["git_origin"]
    assert result["git_branch"] != "master"


@pytest.mark.asyncio
async def test_check_remotes(test_token: str) -> None:
    set_api_token(test_token)
    config = ForcesConfig(group="herrin", repository_name="product")
    assert await check_remotes(config)

    bad_config = ForcesConfig(group="herrin", repository_name="products")
    assert not await check_remotes(bad_config)


def test_get_repo_name_from_vars() -> None:
    os.environ["REPO_NAME"] = "product"
    assert get_repo_name_from_vars() == "product"


def test_extract_repo_name() -> None:
    assert (
        extract_repo_name("git@gitlab.com:fluidattacks/product.git")
        == "product"
    )
    assert (
        extract_repo_name("https://127.0.0..1:8080/fluidattacks/product")
        == "product"
    )
