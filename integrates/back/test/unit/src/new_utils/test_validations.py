# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from custom_exceptions import (
    ErrorFileNameAlreadyExists,
    InvalidChar,
    InvalidField,
    InvalidFieldLength,
    UnsanitizedInputFound,
)
from db_model.groups.types import (
    GroupFile,
)
from newutils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
    validate_fields,
    validate_file_exists,
    validate_file_name,
    validate_group_name,
    validate_sanitized_csv_input,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_alphanumeric_field() -> None:
    assert validate_alphanumeric_field("one test")
    with pytest.raises(InvalidField):
        assert validate_alphanumeric_field("=test2@")


def test_validate_email_address() -> None:
    assert validate_email_address("test@unittesting.com")
    with pytest.raises(InvalidField):
        assert validate_email_address("testunittesting.com")
        assert validate_email_address("test+1@unittesting.com")


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


@pytest.mark.parametrize(
    "fields",
    [
        ["valid", " =invalid"],
        ["=testfield", "testfield2"],
        ["testfield", "testfiel`d"],
        ["testfield", "<testfield2"],
    ],
)
def test_validate_fields(fields: list) -> None:
    assert not bool(validate_fields(["valid%", " valid="]))
    assert not bool(validate_fields(["testfield", "testfield2"]))
    with pytest.raises(InvalidChar):
        assert validate_fields(fields)


def test_validate_file_exists() -> None:
    file_name = "test1.txt"
    validate_file_exists(
        file_name,
        None,
    )
    group_files = [
        GroupFile(
            description="abc",
            file_name="test2.txt",
            modified_by="user@gmail.com",
        ),
        GroupFile(
            description="xyz",
            file_name="test3.txt",
            modified_by="user@gmail.com",
        ),
    ]
    validate_file_exists(
        file_name=file_name,
        group_files=group_files,
    )
    with pytest.raises(ErrorFileNameAlreadyExists):
        assert validate_file_exists("test2.txt", group_files)
        assert validate_file_exists("test3.txt", group_files)


def test_validate_file_name() -> None:
    validate_file_name("test123.py")
    with pytest.raises(InvalidChar):
        assert validate_file_name("test.test.py")
        assert validate_file_name("test=$invalidname!.py")


def test_validate_group_name() -> None:
    assert not bool(validate_group_name("test"))
    with pytest.raises(InvalidField):
        assert validate_group_name("=test2@")


@pytest.mark.parametrize(
    "field",
    [
        ('"=invalidField"'),
        ("'+invalidField"),
        (",-invalidField"),
        (";@invalidField"),
        ("=invalidField"),
        ("+invalidField"),
        ("-invalidField"),
        ("@invalidField"),
        ("\\ninvalidField"),
    ],
)
def test_validate_sanitized_csv_input(field: str) -> None:
    validate_sanitized_csv_input(
        "validfield@",
        "valid+field",
        "valid field",
        "http://localhost/bWAPP/sqli_1.php",
    )
    with pytest.raises(UnsanitizedInputFound):
        assert validate_sanitized_csv_input(field)
