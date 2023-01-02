from custom_exceptions import (
    ErrorFileNameAlreadyExists,
    InvalidChar,
    InvalidCommitHash,
    InvalidField,
    InvalidFieldChange,
    InvalidFieldLength,
    InvalidReportFilter,
    InvalidSpacesField,
    NumberOutOfRange,
    UnsanitizedInputFound,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.groups.types import (
    GroupFile,
)
from newutils.validations import (
    has_sequence,
    validate_alphanumeric_field,
    validate_alphanumeric_field_deco,
    validate_commit_hash_deco,
    validate_email_address,
    validate_email_address_deco,
    validate_field_length,
    validate_field_length_deco,
    validate_fields,
    validate_fields_deco,
    validate_file_exists,
    validate_file_exists_deco,
    validate_file_name,
    validate_file_name_deco,
    validate_finding_id_deco,
    validate_finding_title_change_policy_deco,
    validate_group_language_deco,
    validate_group_name,
    validate_group_name_deco,
    validate_include_lowercase_deco,
    validate_include_number_deco,
    validate_int_range,
    validate_int_range_deco,
    validate_sanitized_csv_input,
    validate_sanitized_csv_input_deco,
    validate_sequence_deco,
    validate_space_field_deco,
    validate_start_letter_deco,
    validate_string_length_between_deco,
    validate_symbols,
    validate_symbols_deco,
)
import pytest
from typing import (
    NamedTuple,
    Optional,
    Tuple,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_alphanumeric_field() -> None:
    assert validate_alphanumeric_field("one test")
    with pytest.raises(InvalidField):
        assert validate_alphanumeric_field("=test2@")


def test_validate_alphanumeric_field_deco() -> None:
    @validate_alphanumeric_field_deco("field")
    def decorated_func(field: str) -> str:
        return field

    assert decorated_func(field="one test")
    with pytest.raises(InvalidField):
        decorated_func(field="=test2@")


def test_validate_email_address() -> None:
    assert validate_email_address("test@unittesting.com")
    with pytest.raises(InvalidField):
        assert validate_email_address("testunittesting.com")
        assert validate_email_address("test+1@unittesting.com")


def test_validate_email_address_deco() -> None:
    @validate_email_address_deco("email")
    def decorated_func(email: str) -> str:
        return email

    assert decorated_func(email="test@unittesting.com")

    class Email(NamedTuple):
        address: str

    @validate_email_address_deco("email_test.address")
    def decorated_func_obj(email_test: Email) -> Email:
        return email_test

    email = Email(address="test@unittesting.com")
    assert decorated_func_obj(email_test=email)
    with pytest.raises(InvalidField):

        decorated_func(email="testunittesting.com")
        decorated_func(email="test+1@unittesting.com")


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


def test_validate_field_length_deco() -> None:
    @validate_field_length_deco(
        "test_string", limit=2, is_greater_than_limit=True
    )
    @validate_field_length_deco("test_string", limit=12)
    def decorated_func(test_string: str) -> str:
        return test_string

    assert decorated_func(test_string="testlength")
    with pytest.raises(InvalidFieldLength):

        @validate_field_length_deco(
            "test_string", limit=11, is_greater_than_limit=True
        )
        @validate_field_length_deco("test_string", limit=9)
        def decorated_func_failed(test_string: str) -> str:
            return test_string

        decorated_func_failed(test_string="testLength")


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


def test_validate_fields_deco() -> None:
    @validate_fields_deco(["field1", "field2"])
    def decorated_func(field1: str, field2: str) -> str:
        return field1 + field2

    assert decorated_func(field1="valid%", field2=" valid=")
    assert decorated_func(field1="testfield", field2="testfield2")
    with pytest.raises(InvalidChar):
        decorated_func(field1="valid", field2=" =invalid")
        decorated_func(field1="=testfield", field2="testfield2")
        decorated_func(field1="testfield", field2="testfiel`d")
        decorated_func(field1="testfield", field2="<testfield2")


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


def test_validate_file_exists_deco() -> None:
    file_name = "test1.txt"

    @validate_file_exists_deco("file_name", None)
    def decorated_func(file_name: str) -> str:
        return file_name

    assert decorated_func(file_name=file_name)

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

    @validate_file_exists_deco("file_name", "group_files")
    def decorated_func_group(
        file_name: str, group_files: Optional[list[GroupFile]]
    ) -> Tuple:
        return (file_name, group_files)

    assert decorated_func_group(
        file_name=file_name,
        group_files=group_files,
    )
    with pytest.raises(ErrorFileNameAlreadyExists):

        decorated_func_group(file_name="test2.txt", group_files=group_files)
        decorated_func_group(file_name="test3.txt", group_files=group_files)


def test_validate_file_name() -> None:
    validate_file_name("test123.py")
    with pytest.raises(InvalidChar):
        assert validate_file_name("test.test.py")  # type: ignore
        assert validate_file_name("test=$invalidname!.py")  # type: ignore


def test_validate_file_name_deco() -> None:
    @validate_file_name_deco("file_name")
    def decorated_func(file_name: str) -> str:
        return file_name

    assert decorated_func(file_name="test123.py")
    with pytest.raises(InvalidChar):

        decorated_func(file_name="test.test.py")
        decorated_func(file_name="test=$invalidname!.py")


def test_validate_group_name() -> None:
    assert not bool(validate_group_name("test"))  # type: ignore
    with pytest.raises(InvalidField):
        assert validate_group_name("=test2@")  # type: ignore


def test_validate_group_name_deco() -> None:
    @validate_group_name_deco("group")
    def decorated_func(group: str) -> str:
        return group

    assert decorated_func(group="test")
    with pytest.raises(InvalidField):

        decorated_func(group="=test2@")


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


def test_validate_int_range_deco() -> None:
    @validate_int_range_deco(
        "int_value", lower_bound=11, upper_bound=12, inclusive=True
    )
    def decorated_func(int_value: int) -> int:
        return int_value

    assert decorated_func(int_value=12)
    with pytest.raises(NumberOutOfRange):

        @validate_int_range_deco(
            "int_value", lower_bound=11, upper_bound=12, inclusive=False
        )
        def decorated_func_fail(int_value: int) -> int:
            return int_value

        decorated_func_fail(int_value=12)


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
    "field1, field2, field3",
    [
        {
            '"=invalidField"',
            "'not_check",
            "'+invalidField",
        },
        {
            ",-invalidField",
            "not_check",
            ";@invalidField",
        },
        {
            "-invalidField",
            "not_check",
            "@invalidField",
        },
        {
            "\\ninvalidField",
            "not_check",
            '"=invalidField"',
        },
    ],
)
def test_validate_sanitized_csv_input_deco(
    field1: str, field2: str, field3: str
) -> None:
    @validate_sanitized_csv_input_deco(field_names=["field1", "field3"])
    def decorated_func(field1: str, field2: str, field3: str) -> str:
        return field1 + field2 + field3

    assert decorated_func(
        field1="validfield@",
        field2="not_check",
        field3="valid field",
    )
    with pytest.raises(UnsanitizedInputFound):
        decorated_func(
            field1=field1,
            field2=field2,
            field3=field3,
        )


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


def test_validate_sequence_deco() -> None:
    @validate_sequence_deco("value")
    def decorated_func(value: str) -> str:
        return value

    assert decorated_func(value="a1221b")
    with pytest.raises(InvalidReportFilter):
        decorated_func(value="aabcc")


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


@pytest.mark.parametrize(
    "value,should_fail",
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
def test_validate_symbols_deco(value: str, should_fail: bool) -> None:
    @validate_symbols_deco("value")
    def decorated_func(value: str) -> str:
        return value

    if should_fail:
        with pytest.raises(InvalidReportFilter):
            decorated_func(value=value)
    else:
        assert decorated_func(value=value)


def test_validate_finding_id_deco() -> None:
    @validate_finding_id_deco("finding_id")
    def decorated_func(finding_id: str) -> str:
        return finding_id

    assert decorated_func(finding_id="12345678-1234-1234-1234-1234567890ab")

    with pytest.raises(InvalidField):
        decorated_func(finding_id="invalid_finding_id")
        decorated_func(finding_id="12345678-1234-1234-1234-1234567890az")
        decorated_func(finding_id="12345678-1234-1234-1234-1234567890a")


@pytest.mark.parametrize(
    "language, should_fail",
    [
        ("en", False),
        ("ES", False),
        ("fr", True),
        ("", True),
        (123, True),
    ],
)
def test_validate_group_language(language: str, should_fail: bool) -> None:
    @validate_group_language_deco("value")
    def decorated_func(value: str) -> str:
        return value

    if should_fail:
        with pytest.raises(InvalidField):
            decorated_func(value=language)
    else:
        assert decorated_func(value=language)


def test_validate_space_field_deco() -> None:
    @validate_space_field_deco("field")
    def decorated_func(field: str) -> str:
        return field

    # Test valid input
    assert decorated_func(field="test")

    # Test invalid input
    with pytest.raises(InvalidSpacesField):
        decorated_func(field="  ")


def test_validate_string_length_between_deco() -> None:
    @validate_string_length_between_deco(
        "field", inclusive_lower_bound=4, inclusive_upper_bound=8
    )
    def decorated_func(field: str) -> str:
        return field

    # Test valid input
    assert decorated_func(field="field")

    # Test invalid input
    with pytest.raises(InvalidFieldLength):
        decorated_func(field="longerfield")


def test_validate_title_change_deco() -> None:
    @validate_finding_title_change_policy_deco(
        "old_title_field",
        "new_title_field",
        "status_field",
    )
    def decorated_func(
        old_title_field: str, new_title_field: str, status_field: str
    ) -> str:
        return old_title_field + new_title_field + status_field

    # Test valid input
    assert decorated_func(
        old_title_field="old_title",
        new_title_field="new_title",
        status_field=FindingStateStatus.CREATED,
    )

    # Test invalid input
    with pytest.raises(InvalidFieldChange):
        decorated_func(
            old_title_field="old_title",
            new_title_field="new_title",
            status_field=FindingStateStatus.APPROVED,
        )


def test_validate_commit_hash_deco() -> None:
    @validate_commit_hash_deco(
        "comm",
    )
    def decorated_func(comm: str) -> str:
        return comm

    decorated_func(comm="da39a3ee5e6b4b0d3255bfef95601890afd80709")
    decorated_func(
        comm="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )

    with pytest.raises(InvalidCommitHash):
        decorated_func(comm="invalid Hash")


def test_validate_start_letter_deco() -> None:
    @validate_start_letter_deco(
        "field",
    )
    def decorated_func(field: str) -> str:
        return field

    decorated_func(field="abc123")

    with pytest.raises(InvalidReportFilter):
        decorated_func(field="123abc")


def test_validate_include_number_deco() -> None:
    @validate_include_number_deco(
        "field",
    )
    def decorated_func(field: str) -> str:
        return field

    decorated_func(field="abc123")

    with pytest.raises(InvalidReportFilter):
        decorated_func(field="abcdef")


def test_validate_include_lowercase_deco() -> None:
    @validate_include_lowercase_deco(
        "field",
    )
    def decorated_func(field: str) -> str:
        return field

    decorated_func(field="abc123")

    with pytest.raises(InvalidReportFilter):
        decorated_func(field="ABC123")
