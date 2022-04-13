from . import (
    get_result_1,
    get_result_2,
)
from custom_exceptions import (
    CredentialNotFound,
)
from dataloaders import (
    get_new_context,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_git_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_update_git_root(populate: bool, email: str) -> None:
    assert populate
    cred_id = "3912827d-2b35-4e08-bd35-1bb24457951d"
    cred_new_name = "Edited SSH Key"
    group_name: str = "group1"
    result: Dict[str, Any] = await get_result_1(
        user=email,
        group=group_name,
        credential_id=cred_id,
        credential_name=cred_new_name,
    )
    assert "errors" not in result
    assert result["data"]["updateGitRoot"]["success"]

    loaders = get_new_context()
    cred = await loaders.credential.load((group_name, cred_id))
    assert cred.state.name == cred_new_name


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_git_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_update_git_root_new_cred(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    cred_id = "1a5dacda-1d52-465c-9158-f6fd5dfe0998"
    root_id = "9059f0cb-3b55-404b-8fc5-627171f424ad"
    result: Dict[str, Any] = await get_result_2(
        user=email,
        group=group_name,
        root_id=root_id,
        credential_id=cred_id,
    )
    assert "errors" not in result
    assert result["data"]["updateGitRoot"]["success"]

    loaders = get_new_context()
    with pytest.raises(CredentialNotFound):
        await loaders.credential.load((group_name, cred_id))

    root = await loaders.root.load((group_name, root_id))
    assert root.cloning.status.value == "FAILED"
    assert root.cloning.reason == "Credentials does not work"
