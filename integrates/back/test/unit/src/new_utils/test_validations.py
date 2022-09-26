# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from custom_exceptions import (
    ErrorFileNameAlreadyExists,
    InvalidChar,
    InvalidField,
    InvalidFieldLength,
    InvalidReportFilter,
    NumberOutOfRange,
    UnsanitizedInputFound,
)
from db_model.groups.types import (
    GroupFile,
)
from newutils.validations import (
    has_sequence,
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
    validate_fields,
    validate_file_exists,
    validate_file_name,
    validate_group_name,
    validate_int_range,
    validate_sanitized_csv_input,
    validate_symbols,
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
    assert not bool(validate_fields(["valid%", " valid="]))  # type: ignore
    assert not bool(
        validate_fields(["testfield", "testfield2"])  # type: ignore
    )
    with pytest.raises(InvalidChar):
        assert validate_fields(fields)  # type: ignore


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
        assert validate_file_exists("test2.txt", group_files)  # type: ignore
        assert validate_file_exists("test3.txt", group_files)  # type: ignore


def test_validate_file_name() -> None:
    validate_file_name("test123.py")
    with pytest.raises(InvalidChar):
        assert validate_file_name("test.test.py")  # type: ignore
        assert validate_file_name("test=$invalidname!.py")  # type: ignore


def test_validate_group_name() -> None:
    assert not bool(validate_group_name("test"))  # type: ignore
    with pytest.raises(InvalidField):
        assert validate_group_name("=test2@")  # type: ignore


@pytest.mark.parametrize(
    "value, lower_bound, upper_bound, inclusive",
    [
        (10, 11, 12, True),
        (10, 11, 12, False),
    ],
)
def test_validate_int_range(
    value: int, lower_bound: int, upper_bound: int, inclusive: bool
) -> None:
    with pytest.raises(NumberOutOfRange):
        assert validate_int_range(
            value, lower_bound, upper_bound, inclusive  # type: ignore
        )


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
        assert validate_sanitized_csv_input(field)  # type: ignore


@pytest.mark.parametrize(
    ["value", "length", "should_fail"],
    [
        ("a123b", 3, True),
        ("a123b", 4, False),
        ("a876b", 3, True),
        ("a876b", 4, False),
        ("aabcc", 3, True),
        ("aabcc", 4, False),
        ("ayxwc", 3, True),
        ("ayxwc", 4, False),
        ("aDEFc", 3, True),
        ("aDEFc", 4, False),
        ("aQPOc", 3, True),
        ("aQPOc", 4, False),
        ("a1221b", 3, False),
        ("a123321b", 4, False),
        ("a3455431b", 4, False),
        ("a1357b", 4, False),
        ("a9753b", 4, False),
        ("acdefghijklabcc", 7, True),
    ],
)
def test_has_sequence(value: str, length: int, should_fail: bool) -> None:
    assert has_sequence(value, length) == should_fail


@pytest.mark.parametrize(
    ["value", "should_fail"],
    [
        ("a123b", True),
        ("a'123b", False),
        ("a~876b", False),
        ("a87:6b", False),
        ("aa;bcc", False),
        ("aa<bcc", False),
        ("ayx%wc", False),
        ("ay>xwc", False),
        ("aDEFc", True),
        ("aDE=Fc", False),
        ("aQP@Oc", False),
        ("aQP-Oc", False),
        ("a12]21b", False),
        ("a123+321b", False),
        ("a34^55431b", False),
        ('a1"357b', False),
        ("a97?53b", False),
    ],
)
def test_validate_symbols(value: str, should_fail: bool) -> None:
    if should_fail:
        with pytest.raises(InvalidReportFilter):
            assert validate_symbols(value)  # type: ignore
    else:
        assert validate_symbols(value) is None  # type: ignore
