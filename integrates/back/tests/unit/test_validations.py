from custom_exceptions import (
    InactiveRoot,
    InvalidChar,
    InvalidField,
    InvalidFieldLength,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.types import (
    RootItem,
)
from newutils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
    validate_fields,
    validate_file_name,
    validate_group_name,
)
import pytest
from roots.validations import (
    is_exclude_valid,
    is_valid_git_branch,
    is_valid_ip,
    is_valid_url,
    validate_active_root,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_validate_active_root() -> None:
    loaders = get_new_context()
    active_root: RootItem = await loaders.root.load(
        ("oneshottest", "8493c82f-2860-4902-86fa-75b0fef76034")
    )
    validate_active_root(active_root)
    inactive_root: RootItem = await loaders.root.load(
        ("asgard", "814addf0-316c-4415-850d-21bd3783b011")
    )
    with pytest.raises(InactiveRoot):
        validate_active_root(inactive_root)


def test_validate_fields() -> None:
    assert not bool(validate_fields(["valid%", " valid="]))
    assert not bool(validate_fields(["testfield", "testfield2"]))
    with pytest.raises(InvalidChar):
        assert validate_fields(["valid", " =invalid"])
        assert validate_fields(["=testfield", "testfield2"])
        assert validate_fields(["testfield", "testfiel'd"])
        assert validate_fields(["testfield", "<testfield2"])


def test_validate_field_length() -> None:
    assert validate_field_length("testlength", limit=12)
    assert validate_field_length(
        "testlength", limit=2, is_greater_than_limit=True
    )
    with pytest.raises(InvalidFieldLength):
        validate_field_length("testlength", limit=9)
        validate_field_length(
            "testlength", limit=11, is_greater_than_limit=True
        )


def test_validate_email_address() -> None:
    assert validate_email_address("test@unittesting.com")
    with pytest.raises(InvalidField):
        assert validate_email_address("testunittesting.com")
        assert validate_email_address("test+1@unittesting.com")


def test_validate_group_name() -> None:
    assert not bool(validate_group_name("test"))
    with pytest.raises(InvalidField):
        assert validate_group_name("=test2@")


def test_validate_alphanumeric_field() -> None:
    assert validate_alphanumeric_field("one test")
    with pytest.raises(InvalidField):
        assert validate_alphanumeric_field("=test2@")


def test_validate_file_name() -> None:
    assert validate_file_name("test123.py")
    with pytest.raises(InvalidChar):
        assert validate_file_name("test.test.py")
        assert validate_file_name("test=$invalidname!.py")


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
    repo_url: str = "https://fluidattacks.com/product"
    assert is_exclude_valid(
        ["*/test.py", "production/test.py", "test/product/test.py"], repo_url
    )
    assert not is_exclude_valid(["Product/test.py"], repo_url)
    assert not is_exclude_valid(["product/**/test.py"], repo_url)
