from custom_exceptions import (
    InvalidParameter,
)
from dataloaders import (
    get_new_context,
)
from db_model.credentials.types import (
    CredentialItem,
)
from db_model.enums import (
    CredentialType,
)
import pytest
from roots import (
    domain as roots_domain,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_root_id_by_nickname() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    group_roots_loader = loaders.group_roots
    group_roots = await group_roots_loader.load(group_name)
    root_id = roots_domain.get_root_id_by_nickname(
        "product", group_roots, only_git_roots=True
    )
    assert root_id == "4039d098-ffc5-4984-8ed3-eb17bca98e19"


async def test_get_last_cloning_successful() -> None:
    loaders = get_new_context()
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    item = await roots_domain.get_last_cloning_successful(loaders, root_id)
    assert item.status == "OK"


def test_format_credential_key() -> None:
    key_1 = "VGVzdCBTU0g="
    expected_key_1 = "VGVzdCBTU0gK"
    assert (
        roots_domain._format_credential_key(
            key_type=CredentialType.SSH, key=key_1
        )
        == expected_key_1
    )
    assert (
        roots_domain._format_credential_key(
            key_type=CredentialType.SSH, key=expected_key_1
        )
        == expected_key_1
    )


def test_format_root_credential() -> None:
    credentials = {"key": "VGVzdCBTU0ggS2V5bgo=", "name": "", "type": "SSH"}
    with pytest.raises(InvalidParameter):
        roots_domain._format_root_credential(
            credentials=credentials,
            group_name="group1",
            user_email="admin@gmail.com",
            root_id="f052c6ca-587b-48ee-a0f7-299f0dd8402a",
        )

    credentials.update({"name": "SSH Key"})
    assert isinstance(
        roots_domain._format_root_credential(
            credentials=credentials,
            group_name="group1",
            user_email="admin@gmail.com",
            root_id="f052c6ca-587b-48ee-a0f7-299f0dd8402a",
        ),
        CredentialItem,
    )


@pytest.mark.parametrize(
    "url_input,expected",
    [
        (
            (
                "https://mycompany@dev.azure.com/"
                "mycompany/myproject/_git/myproject"
            ),
            "https://dev.azure.com/mycompany/myproject/_git/myproject",
        ),
        (
            (
                "https://mycompany@dev.azure.com:30/"
                "mycompany/myproject/_git/myproject"
            ),
            "https://dev.azure.com:30/mycompany/myproject/_git/myproject",
        ),
        (
            "ssh://git@ssh.dev.azure.com:v3/fluidattacks-product/demo/demo",
            "ssh://git@ssh.dev.azure.com:v3/fluidattacks-product/demo/demo",
        ),
        (
            "https://dev.azure.com/mycompany/myproject/_git/myproject",
            "https://dev.azure.com/mycompany/myproject/_git/myproject",
        ),
    ],
)
def test_format_url(url_input: str, expected: str) -> None:
    assert roots_domain.format_git_repo_url(url_input) == expected
