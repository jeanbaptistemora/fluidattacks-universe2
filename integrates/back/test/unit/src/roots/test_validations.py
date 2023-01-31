from custom_exceptions import (
    InactiveRoot,
    InvalidChar,
    InvalidGitCredentials,
    InvalidGitRoot,
    InvalidRootComponent,
    InvalidUrl,
    RepeatedRootNickname,
    RequiredCredentials,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    HttpsSecret,
    OauthAzureSecret,
    OauthBitbucketSecret,
    SshSecret,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.roots.types import (
    Root,
    RootRequest,
)
from newutils.datetime import (
    get_now_minus_delta,
)
import pytest
from roots.validations import (
    is_exclude_valid,
    is_git_unique,
    is_valid_git_branch,
    is_valid_ip,
    is_valid_url,
    validate_active_root,
    validate_active_root_deco,
    validate_component,
    validate_credential_in_organization,
    validate_git_access,
    validate_git_credentials_oauth,
    validate_git_root,
    validate_git_root_deco,
    validate_nickname,
    validate_nickname_deco,
    validate_nickname_is_unique_deco,
    working_credentials,
)
from typing import (
    Tuple,
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


async def test_validate_active_root_deco() -> None:
    @validate_active_root_deco("root")
    def decorated_func(root: Root) -> Root:
        return root

    loaders = get_new_context()
    active_root: Root = await loaders.root.load(
        RootRequest("oneshottest", "8493c82f-2860-4902-86fa-75b0fef76034")
    )

    assert decorated_func(root=active_root)

    inactive_root: Root = await loaders.root.load(
        RootRequest("asgard", "814addf0-316c-4415-850d-21bd3783b011")
    )
    with pytest.raises(InactiveRoot):
        decorated_func(root=inactive_root)


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
    with pytest.raises(InvalidUrl):
        await validate_component(
            loaders, git_root, "://app.invalid.com:66000/test"
        )
    with pytest.raises(InvalidUrl):
        await validate_component(
            loaders, url_root, "://app.invalid.com:66000/test"
        )


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
    repo_git: str = "git@gitlab.com:fluidattacks/universe.git"
    assert is_exclude_valid(
        ["*/test.py", "production/test.py", "test/universe/test.py"], repo_url
    )
    assert is_exclude_valid(
        ["*/test.py", "production/test.py", "test/universe/test.py"], repo_git
    )
    assert not is_exclude_valid(["Universe/test.py"], repo_url)
    assert not is_exclude_valid(["universe/**/test.py"], repo_url)


async def test_valid_git_root() -> None:

    loaders = get_new_context()
    root: Root = await loaders.root.load(
        RootRequest("unittesting", "4039d098-ffc5-4984-8ed3-eb17bca98e19")
    )
    validate_git_root(root)
    ip_root: Root = await loaders.root.load(
        RootRequest("oneshottest", "d312f0b9-da49-4d2b-a881-bed438875e99")
    )
    with pytest.raises(InvalidGitRoot):
        validate_git_root(ip_root)


async def test_valid_git_root_deco() -> None:
    @validate_git_root_deco("root")
    def decorated_func(root: Root) -> Root:
        return root

    loaders = get_new_context()
    root: Root = await loaders.root.load(
        RootRequest("unittesting", "4039d098-ffc5-4984-8ed3-eb17bca98e19")
    )

    assert decorated_func(root=root)

    ip_root: Root = await loaders.root.load(
        RootRequest("oneshottest", "d312f0b9-da49-4d2b-a881-bed438875e99")
    )
    with pytest.raises(InvalidGitRoot):
        decorated_func(root=ip_root)


async def test_validate_git_access() -> None:
    await validate_git_access(
        url="https://app.fluidattacks.com",
        branch="trunk1",
        secret=OauthBitbucketSecret(
            brefresh_token="token",
            access_token="access_token",
            valid_until=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
        ),
        loaders=get_new_context(),
    )
    with pytest.raises(InvalidUrl):
        await validate_git_access(
            url="https://app.fluidattacks.com:67000",
            branch="trunk",
            secret=SshSecret(key="test_key"),
            loaders=get_new_context(),
        )
    with pytest.raises(InvalidGitCredentials):
        await validate_git_access(
            url="https://app.fluidattacks.com",
            branch="trunk2",
            secret=OauthAzureSecret(
                arefresh_token="CFCzdCBTU0gK",
                redirect_uri="",
                access_token="DEDzdCBTU0gK",
                valid_until=get_now_minus_delta(hours=1),
            ),
            loaders=get_new_context(),
            organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            credential_id="5990e0ec-dc8f-4c9a-82cc-9da9fbb35c11",
        )
    with pytest.raises(InvalidGitCredentials):
        await validate_git_access(
            url="https://app.fluidattacks.com",
            branch="trunk1",
            secret=HttpsSecret(
                user="user",
                password="password",
            ),
            loaders=get_new_context(),
        )


async def test_validate_credential_in_organization() -> None:
    with pytest.raises(InvalidGitCredentials):
        await validate_credential_in_organization(
            loaders=get_new_context(),
            credential_id="test_id",
            organization_id="test_org",
        )


async def test_working_credentials() -> None:
    with pytest.raises(RequiredCredentials):
        await working_credentials(
            url="https://app.fluidattacks.com",
            branch="trunk",
            credentials=None,
            loaders=get_new_context(),
        )


async def test_is_git_unique() -> None:
    loaders = get_new_context()
    organization: Organization = await loaders.organization.load("okada")
    roots = tuple(await loaders.organization_roots.load(organization.name))
    assert not is_git_unique(
        url="https://gitlab.com/fluidattacks/universe",
        branch="master",
        group_name="unittesting2",
        roots=roots,
    )
    assert not is_git_unique(
        url="https://gitlab.com/fluidattacks/universe",
        branch="main",
        group_name="unittesting",
        roots=roots,
    )


def test_validate_nickname() -> None:
    validate_nickname(nickname="valid-username_1")
    with pytest.raises(InvalidChar):
        validate_nickname(nickname="invalidusername!")


def test_validate_nickname_deco() -> None:
    @validate_nickname_deco("nickname")
    def decorated_func(nickname: str) -> str:
        return nickname

    assert decorated_func(nickname="valid-username_1")
    with pytest.raises(InvalidChar):
        decorated_func(nickname="invalidusername!")


async def test_validate_git_credentials_oauth() -> None:
    with pytest.raises(InvalidGitCredentials):
        await validate_git_credentials_oauth(
            repo_url="https://fluidattacks.com/universe",
            branch="trunk",
            loaders=get_new_context(),
            credential_id="158d1f7f-65c5-4c79-85e3-de3acfe03774",
            organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
        )


async def test_validate_nickname_is_unique_deco() -> None:
    @validate_nickname_is_unique_deco(
        nickname_field="nickname",
        roots_fields="roots",
        old_nickname_field="old_nickname",
    )
    def decorated_func(
        nickname: str, roots: tuple[Root, ...], old_nickname: str
    ) -> Tuple:
        return (nickname, roots, old_nickname)

    loaders = get_new_context()
    root: Root = await loaders.root.load(
        RootRequest("unittesting", "4039d098-ffc5-4984-8ed3-eb17bca98e19")
    )
    assert decorated_func(
        nickname="valid-username_1",
        roots=(root,),
        old_nickname="valid-username_2",
    )
    with pytest.raises(RepeatedRootNickname):
        decorated_func(
            nickname="universe",
            roots=(root,),
            old_nickname="valid-username_2",
        )
