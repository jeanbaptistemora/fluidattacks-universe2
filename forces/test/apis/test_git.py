from forces.apis.git import (
    check_remotes,
    extract_repo_name,
    get_repo_name_from_vars,
    get_repository_metadata,
)
from forces.apis.integrates import (
    set_api_token,
)
from forces.model import (
    ForcesConfig,
)
import os
import pytest


@pytest.mark.asyncio
def test_get_repository_metadata_test() -> None:
    result = get_repository_metadata(repo_path=".")
    assert result["git_repo"] == "universe"
    assert "fluidattacks/universe" in result["git_origin"]
    assert result["git_branch"] != "trunk"


@pytest.mark.asyncio
async def test_check_remotes(test_token: str) -> None:
    set_api_token(test_token)
    config = ForcesConfig(group="unittesting", repository_name="universe")
    assert await check_remotes(config)

    bad_config = ForcesConfig(group="unittesting", repository_name="universes")
    assert not await check_remotes(bad_config)


def test_get_repo_name_from_vars() -> None:
    os.environ["REPO_NAME"] = "universe"
    assert get_repo_name_from_vars() == "universe"


def test_extract_repo_name() -> None:
    assert (
        extract_repo_name("git@gitlab.com:fluidattacks/universe.git")
        == "universe"
    )
    assert (
        extract_repo_name("https://127.0.0..1:8080/fluidattacks/universe")
        == "universe"
    )
