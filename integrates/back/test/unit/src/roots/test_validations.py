from custom_exceptions import (
    InactiveRoot,
    InvalidRootComponent,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.types import (
    Root,
    RootRequest,
)
import pytest
from roots.validations import (
    is_exclude_valid,
    is_valid_git_branch,
    is_valid_ip,
    is_valid_url,
    validate_active_root,
    validate_component,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_validate_active_root() -> None:
    loaders = get_new_context()
    active_root: Root = await loaders.root.load(
        RootRequest("oneshottest", "8493c82f-2860-4902-86fa-75b0fef76034")
    )
    validate_active_root(active_root)
    inactive_root: Root = await loaders.root.load(
        RootRequest("asgard", "814addf0-316c-4415-850d-21bd3783b011")
    )
    with pytest.raises(InactiveRoot):
        validate_active_root(inactive_root)


async def test_validate_component() -> None:
    loaders = get_new_context()
    git_root: Root = await loaders.root.load(
        RootRequest("unittesting", "4039d098-ffc5-4984-8ed3-eb17bca98e19")
    )
    await validate_component(
        loaders, git_root, "https://app.fluidattacks.com/test"
    )
    url_root: Root = await loaders.root.load(
        RootRequest("oneshottest", "8493c82f-2860-4902-86fa-75b0fef76034")
    )
    await validate_component(
        loaders, url_root, "https://app.fluidattacks.com:443/test"
    )
    ip_root: Root = await loaders.root.load(
        RootRequest("oneshottest", "d312f0b9-da49-4d2b-a881-bed438875e99")
    )
    await validate_component(loaders, ip_root, "127.0.0.1:8080/test")
    with pytest.raises(InvalidRootComponent):
        await validate_component(
            loaders, git_root, "https://app.invalid.com/test"
        )
        await validate_component(
            loaders, url_root, "https://app.fluidattacks.com:440"
        )
        await validate_component(loaders, ip_root, "127.0.0.1/test")


def test_is_valid_url() -> None:
    assert is_valid_url("https://fluidattacks.com/")
    assert is_valid_url("ssh://git@ssh.dev.azure.com:v3/company/project/")
    assert not is_valid_url("randomstring")


def test_is_valid_git_branch() -> None:
    assert is_valid_git_branch("master")
    assert not is_valid_git_branch("( ͡° ͜ʖ ͡°)")


def test_is_valid_ip() -> None:
    # FP: local testing
    assert is_valid_ip("8.8.8.8")  # NOSONAR
    assert not is_valid_ip("randomstring")


def test_is_exclude_valid() -> None:
    repo_url: str = "https://fluidattacks.com/universe"
    assert is_exclude_valid(
        ["*/test.py", "production/test.py", "test/universe/test.py"], repo_url
    )
    assert not is_exclude_valid(["Universe/test.py"], repo_url)
    assert not is_exclude_valid(["universe/**/test.py"], repo_url)
