import bleach  # type: ignore
from custom_exceptions import (
    IncompleteSeverity,
    InvalidChar,
    InvalidCvssVersion,
    InvalidField,
    InvalidFieldLength,
    InvalidMarkdown,
)
from db_model.findings.enums import (
    FindingCvssVersion,
)
from db_model.findings.types import (
    Finding20Severity,
    Finding31Severity,
)
from newutils import (
    utils,
)
import re
from typing import (
    List,
    Set,
)


def validate_email_address(email: str) -> bool:
    if "+" in email:
        raise InvalidField("email address")
    try:
        check_field(
            email,
            r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",
        )
        return True
    except InvalidChar as ex:
        raise InvalidField("email address") from ex


def validate_fields(fields: List[str]) -> None:
    allowed_chars = (
        r"a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ \t\n\r\x0b\x0c(),./:;%@_$#*=\?-"
    )
    regex = fr'^[{allowed_chars.replace("=", "")}][{allowed_chars}]*$'
    for field in map(str, fields):
        if field:
            check_field(field, regex)


def validate_url(url: str) -> None:
    clean_url: str = url
    encoded_chars_whitelist: List[str] = ["%20"]
    for encoded_char in encoded_chars_whitelist:
        clean_url = clean_url.replace(encoded_char, "")

    if clean_url:
        allowed_chars = r"a-zA-Z0-9(),./:;@_$#=\?-"
        check_field(
            clean_url,
            fr'^[{allowed_chars.replace("=", "")}]+[{allowed_chars}]*$',
        )


def validate_file_name(name: str) -> bool:
    """Verify that filename has valid characters."""
    name = str(name)
    name_len = len(name.split("."))
    if name_len <= 2:
        is_valid = bool(
            re.search("^[A-Za-z0-9!_.*'()&$@=;:+,? -]*$", str(name))
        )
    else:
        is_valid = False
    return is_valid


def check_field(field: str, regexp: str) -> None:
    if not re.match(regexp, field.strip()):
        raise InvalidChar()


def validate_field_length(
    field: str, limit: int, is_greater_than_limit: bool = False
) -> bool:
    """
    if is_greater_than_limit equals True,
    it means we are checking if field > limit
    """
    if (len(field) > limit) != is_greater_than_limit:
        raise InvalidFieldLength()
    return True


def validate_finding_id(finding_id: str) -> None:
    if not re.match(
        r"[0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab]"
        r"[0-9A-Za-z]{3}-[0-9A-Za-z]{12}|\d+",
        finding_id,
    ):
        raise InvalidField("finding id")


def validate_group_name(group_name: str) -> None:
    if not group_name.isalnum():
        raise InvalidField("group name")


def validate_markdown(text: str) -> str:
    """
    Escapes special characters and accepts only
    the use of certain html tags
    """
    allowed_tags = [
        "a",
        "b",
        "br",
        "div",
        "dl",
        "dt",
        "em",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "img",
        "li",
        "ol",
        "p",
        "small",
        "strong",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "tr",
        "tt",
        "ul",
    ]
    allowed_attrs = {
        "a": ["href", "rel", "target"],
        "img": ["src", "alt", "width", "height"],
    }
    cleaned = bleach.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attrs,
    )
    if text != cleaned:
        raise InvalidMarkdown()

    return cleaned


def validate_missing_severity_field_names(
    field_names: Set[str], css_version: str
) -> None:
    if css_version == FindingCvssVersion.V20.value:
        missing_field_names = {
            utils.snakecase_to_camelcase(field)
            for field in Finding20Severity._fields
            if field not in field_names
        }
    elif css_version == FindingCvssVersion.V31.value:
        missing_field_names = {
            utils.snakecase_to_camelcase(field)
            for field in Finding31Severity._fields
            if field not in field_names
        }
    else:
        raise InvalidCvssVersion()
    if missing_field_names:
        raise IncompleteSeverity(missing_field_names)


def validate_string_length_between(
    string: str,
    inclusive_lower_bound: int,
    inclusive_upper_bound: int,
) -> None:
    if not inclusive_lower_bound <= len(string) <= inclusive_upper_bound:
        raise InvalidFieldLength()


def validate_alphanumeric_field(field: str) -> bool:
    """Optional whitespace separated string, with alphanumeric characters."""
    is_alnum = all(word.isalnum() for word in field.split())
    if is_alnum or field == "-" or not field:
        return True
    raise InvalidField()
