# pylint: disable=too-many-lines
import bleach
from custom_exceptions import (
    DuplicateDraftFound,
    ErrorFileNameAlreadyExists,
    IncompleteSeverity,
    InvalidChar,
    InvalidCommitHash,
    InvalidCvssVersion,
    InvalidField,
    InvalidFieldChange,
    InvalidFieldLength,
    InvalidMarkdown,
    InvalidMinTimeToRemediate,
    InvalidReportFilter,
    InvalidSeverityUpdateValues,
    InvalidSpacesField,
    NumberOutOfRange,
    UnsanitizedInputFound,
)
from db_model.findings.enums import (
    FindingCvssVersion,
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
)
from db_model.groups.types import (
    GroupFile,
)
import functools
import itertools
from newutils import (
    utils,
)
import re
from typing import (
    Any,
    Callable,
    cast,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
)

# Typing
T = TypeVar("T")


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


def validate_email_address_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = get_attr_value(
                field=field, kwargs=kwargs, obj_type=str
            )
            if "+" in field_content:
                raise InvalidField("email address")
            try:
                check_field(
                    field_content,
                    r"^([a-zA-Z0-9_\-\.]+)@"
                    r"([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",
                )
                return func(*args, **kwargs)
            except InvalidChar as ex:
                raise InvalidField("email address") from ex

        return decorated

    return wrapper


def validate_fields(fields: Iterable[str]) -> None:
    allowed_chars = (
        r"a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s'~:;%@&_$#=¡!¿"
        r"\,\.\*\-\?\"\[\]\|\(\)\/\{\}\>\+"
    )
    regex = rf'^[{allowed_chars.replace("=", "")}][{allowed_chars}]*$'
    for field in map(str, fields):
        if field:
            check_field(field, regex)


def validate_fields_deco(fields: Iterable[str]) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            allowed_chars = (
                r"a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s'~:;%@&_$#=¡!¿"
                r"\,\.\*\-\?\"\[\]\|\(\)\/\{\}\>\+"
            )
            regex = rf'^[{allowed_chars.replace("=", "")}][{allowed_chars}]*$'

            for field in fields:
                value = kwargs.get(field)
                if "." in field:
                    obj_name, attr_name = field.split(".")
                    obj = kwargs.get(obj_name)
                    if obj_name in kwargs:
                        field_content = getattr(obj, attr_name)
                        if field_content:
                            check_field(str(field_content), regex)
                if field in kwargs and value:
                    check_field(str(value), regex)

            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_url(url: Optional[str]) -> None:
    clean_url: str = url if url is not None else ""
    encoded_chars_whitelist: List[str] = ["%20"]
    for encoded_char in encoded_chars_whitelist:
        clean_url = clean_url.replace(encoded_char, "")

    if clean_url:
        allowed_chars = r"a-zA-Z0-9(),./:;@_$#=\?-"
        check_field(
            clean_url,
            rf'^[{allowed_chars.replace("=", "")}]+[{allowed_chars}]*$',
        )


def validate_url_deco(url_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            url = get_attr_value(field=url_field, kwargs=kwargs, obj_type=str)
            validate_url(url=url)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_chart_field(param_value: str, param_name: str) -> None:
    is_valid = bool(re.search("^[A-Za-z0-9 #_-]*$", str(param_value)))
    if not is_valid:
        raise InvalidChar(param_name)


def validate_chart_field_deco(
    param_value_field: str, param_name_field: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            param_value = get_attr_value(
                field=param_value_field, kwargs=kwargs, obj_type=str
            )
            param_name = get_attr_value(
                field=param_name_field, kwargs=kwargs, obj_type=str
            )
            is_valid = bool(re.search("^[A-Za-z0-9 #_-]*$", str(param_value)))
            if not is_valid:
                raise InvalidChar(param_name)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_file_name(name: str) -> None:
    """Verify that filename has valid characters. Raises InvalidChar
    otherwise."""
    name = str(name)
    name_len = len(name.split("."))
    if name_len <= 2:
        is_valid = bool(
            re.search("^[A-Za-z0-9!_.*/'()&$@=;:+,? -]*$", str(name))
        )
        if not is_valid:
            raise InvalidChar("filename")
    else:
        raise InvalidChar("filename")


def validate_file_name_deco(field: str) -> Callable:
    """Verify that filename has valid characters. Raises InvalidChar
    otherwise."""

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            name_len = len(field_content.split("."))
            if name_len <= 2:
                is_valid = bool(
                    re.search(
                        "^[A-Za-z0-9!_.*/'()&$@=;:+,? -]*$", str(field_content)
                    )
                )
                if not is_valid:
                    raise InvalidChar("filename")
                return func(*args, **kwargs)
            raise InvalidChar("filename")

        return decorated

    return wrapper


def validate_file_exists(
    file_name: str, group_files: Optional[list[GroupFile]]
) -> None:
    """Verify that file name is not already in group files."""
    if group_files:
        file_to_check = next(
            (
                group_file
                for group_file in group_files
                if group_file.file_name == file_name
            ),
            None,
        )
        if file_to_check is not None:
            raise ErrorFileNameAlreadyExists.new()


def validate_file_exists_deco(
    field_name: str, field_group_files: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            file_name = get_attr_value(
                field=field_name, kwargs=kwargs, obj_type=str
            )
            group_files = get_attr_value(
                field=field_group_files,
                kwargs=kwargs,
                obj_type=list[GroupFile],
            )
            if group_files is not None:
                file_to_check = next(
                    (
                        group_file
                        for group_file in group_files
                        if group_file.file_name == file_name
                    ),
                    None,
                )
                if file_to_check is not None:
                    raise ErrorFileNameAlreadyExists.new()
            return func(*args, **kwargs)

        return decorated

    return wrapper


def check_field(field: str, regexp: str) -> None:
    if not re.match(regexp, field.replace("\n", " ").strip(), re.MULTILINE):
        raise InvalidChar()


def validate_field_length(
    field: str, limit: int, is_greater_than_limit: bool = False
) -> bool:
    """
    if is_greater_than_limit equals True,
    it means we are checking if field > limit
    """
    if field is None or ((len(field) > limit) != is_greater_than_limit):
        raise InvalidFieldLength()
    return True


def validate_field_length_deco(
    field: str, limit: int, is_greater_than_limit: bool = False
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = get_attr_value(
                field=field, kwargs=kwargs, obj_type=str
            )
            if field_content is None:
                return func(*args, **kwargs)
            if (len(field_content) > limit) != is_greater_than_limit:
                raise InvalidFieldLength()
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_finding_id(finding_id: str) -> None:
    if not re.match(
        r"[0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab]"
        r"[0-9A-Za-z]{3}-[0-9A-Za-z]{12}|\d+",
        finding_id,
    ):
        raise InvalidField("finding id")


def validate_finding_id_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if not re.fullmatch(
                r"[0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab]"
                r"[0-9A-Za-z]{3}-[0-9A-Za-z]{12}|\d+",
                field_content,
            ):
                raise InvalidField("finding id")
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_group_language(language: str) -> None:
    if language.upper() not in {"EN", "ES"}:
        raise InvalidField("group language")


def validate_group_language_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            language = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if language.upper() not in {"EN", "ES"}:
                raise InvalidField("group language")
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_group_name(group_name: str) -> None:
    if not group_name.isalnum():
        raise InvalidField("group name")


def validate_group_name_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if not field_content.isalnum():
                raise InvalidField("group name")
            return func(*args, **kwargs)

        return decorated

    return wrapper


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
    cleaned = cleaned.replace("&amp;", "&")
    if text != cleaned:
        raise InvalidMarkdown()

    return cleaned


def validate_markdown_deco(text_field: str) -> Callable:
    """
    Escapes special characters and accepts only
    the use of certain html tags
    """

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            text = get_attr_value(
                field=text_field, kwargs=kwargs, obj_type=str
            )
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
            cleaned = cleaned.replace("&amp;", "&")
            if text != cleaned:
                raise InvalidMarkdown()
            return func(*args, **kwargs)

        return decorated

    return wrapper


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


def validate_missing_severity_field_names_deco(
    field_names_field: str, css_version_field: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            css_version = get_attr_value(
                field=css_version_field, kwargs=kwargs, obj_type=str
            )
            field_names = get_attr_value(
                field=field_names_field, kwargs=kwargs, obj_type=set[str]
            )
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
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_update_severity_values(dictionary: dict) -> None:
    if (
        len(
            list(
                filter(
                    lambda item: item[1] < 0 or item[1] > 10,
                    dictionary.items(),
                )
            )
        )
        > 0
    ):
        raise InvalidSeverityUpdateValues()


def validate_update_severity_values_deco(dictionary_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            dictionary = get_attr_value(
                field=dictionary_field, kwargs=kwargs, obj_type=dict
            )
            if (
                len(
                    list(
                        filter(
                            lambda item: item[1] < 0 or item[1] > 10,
                            dictionary.items(),
                        )
                    )
                )
                > 0
            ):
                raise InvalidSeverityUpdateValues()
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_space_field(field: str) -> None:
    if not re.search(r"\S", field):
        raise InvalidSpacesField


def validate_space_field_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if not re.search(r"\S", field_content):
                raise InvalidSpacesField
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_string_length_between(
    string: str,
    inclusive_lower_bound: int,
    inclusive_upper_bound: int,
) -> None:
    if not inclusive_lower_bound <= len(string) <= inclusive_upper_bound:
        raise InvalidFieldLength()


def validate_string_length_between_deco(
    field: str,
    inclusive_lower_bound: int,
    inclusive_upper_bound: int,
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            string = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if (
                not inclusive_lower_bound
                <= len(string)
                <= inclusive_upper_bound
            ):
                raise InvalidFieldLength()
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_alphanumeric_field(field: str) -> bool:
    """Optional whitespace separated string, with alphanumeric characters."""
    is_alnum = all(word.isalnum() for word in field.split())
    if is_alnum or field == "-" or not field:
        return True
    raise InvalidField()


def validate_alphanumeric_field_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            is_alnum = all(word.isalnum() for word in field_content.split())
            if is_alnum or field_content == "-" or not field_content:
                return func(*args, **kwargs)
            raise InvalidField()

        return decorated

    return wrapper


def validate_finding_title_change_policy(
    old_title: str, new_title: str, status: FindingStateStatus
) -> bool:
    """Blocks finding title changes from going through if the Finding has been
    already approved"""
    if old_title != new_title and status == FindingStateStatus.APPROVED:
        raise InvalidFieldChange(
            fields=["title"],
            reason=(
                "The title of a Finding cannot be edited after "
                "it has been approved"
            ),
        )
    return True


def get_attr_value(field: str, kwargs: dict, obj_type: Type[T]) -> T:
    if "." not in field:
        return cast(T, kwargs.get(field))
    obj_name, obj_attr = field.split(".", 1)
    parts = obj_attr.split(".")
    obj = kwargs.get(obj_name)
    for part in parts:
        value = getattr(obj, part)
        obj = value
        print(part, value, obj)
    if not isinstance(value, obj_type):
        return cast(T, value)
    return value


def validate_finding_title_change_policy_deco(
    old_title_field: str, new_title_field: str, status_field: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            old_title = get_attr_value(
                field=old_title_field, kwargs=kwargs, obj_type=str
            )
            new_title = get_attr_value(
                field=new_title_field, kwargs=kwargs, obj_type=str
            )
            status = cast(FindingStateStatus, kwargs.get(status_field))
            if (
                old_title != new_title
                and status == FindingStateStatus.APPROVED
            ):
                raise InvalidFieldChange(
                    fields=["title"],
                    reason=(
                        "The title of a Finding cannot be edited after "
                        "it has been approved"
                    ),
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_no_duplicate_drafts(
    new_title: str, drafts: Tuple[Finding, ...], findings: Tuple[Finding, ...]
) -> bool:
    """Checks for new draft proposals that are already present in the group,
    returning `True` if there are no duplicates"""
    for draft in drafts:
        if new_title == draft.title:
            raise DuplicateDraftFound(kind="draft")
    for finding in findings:
        if new_title == finding.title:
            raise DuplicateDraftFound(kind="finding")
    return True


def validate_no_duplicate_drafts_deco(
    new_title_field: str, drafts_field: str, findings_field: str
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            new_title = get_attr_value(
                field=new_title_field, kwargs=kwargs, obj_type=str
            )
            drafts = get_attr_value(
                field=drafts_field, kwargs=kwargs, obj_type=tuple[Finding, ...]
            )
            findings = get_attr_value(
                field=findings_field,
                kwargs=kwargs,
                obj_type=tuple[Finding, ...],
            )
            for draft in drafts:
                if new_title == draft.title:
                    raise DuplicateDraftFound(kind="draft")
            for finding in findings:
                print(new_title, finding.title)
                if new_title == finding.title:
                    raise DuplicateDraftFound(kind="finding")
            return func(*args, **kwargs)

        return decorated

    return wrapper


def check_and_set_min_time_to_remediate(
    mttr: Optional[str],
) -> Optional[int]:
    """Makes sure that min_time_to_remediate is either None or a positive
    number and returns it as a Decimal"""
    try:
        if mttr is None:
            return None
        if int(mttr) > 0:
            return int(mttr)
        raise InvalidMinTimeToRemediate()
    except ValueError as error:
        raise InvalidMinTimeToRemediate() from error


def validate_sanitized_csv_input(*fields: str) -> None:
    """Checks for the presence of any character that could be interpreted as
    the start of a formula by a spreadsheet editor according to
    https://owasp.org/www-community/attacks/CSV_Injection"""
    forbidden_characters: Tuple[str, ...] = (
        "-",
        "=",
        "+",
        "@",
        "\t",
        "\r",
        "\n",
        "\\",
    )
    separators: Tuple[str, ...] = ('"', "'", ",", ";")
    fields_union = [field.split() for field in fields]
    fields_flat = list(itertools.chain(*fields_union))
    for field in fields_flat:
        for character in forbidden_characters:
            # match characters at the beginning of string
            if re.match(re.escape(character), field):
                raise UnsanitizedInputFound()
            # check for field separator and quotes
            char_locations: List[int] = [
                match.start()
                for match in re.finditer((re.escape(character)), field)
            ]
            for location in char_locations:
                if any(
                    separator in field[location - 1]
                    for separator in separators
                ):
                    raise UnsanitizedInputFound()


def validate_sanitized_csv_input_deco(field_names: List[str]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(**kwargs: str) -> None:
            """Checks for the presence of any character that could be
            interpreted as the start of a formula by a spreadsheet editor
            according to
            https://owasp.org/www-community/attacks/CSV_Injection"""
            forbidden_characters: Tuple[str, ...] = (
                "-",
                "=",
                "+",
                "@",
                "\t",
                "\r",
                "\n",
                "\\",
            )
            separators: Tuple[str, ...] = ('"', "'", ",", ";")
            fields_to_validate = [
                str(kwargs.get(field))
                if "." not in field
                else str(
                    getattr(
                        kwargs.get(field.split(".")[0]), field.split(".")[1]
                    )
                )
                for field in field_names
            ]
            fields_union = [field.split() for field in fields_to_validate]
            fields_flat = list(itertools.chain(*fields_union))
            for field in fields_flat:
                for character in forbidden_characters:
                    # match characters at the beginning of string
                    if re.match(re.escape(character), field):
                        raise UnsanitizedInputFound()
                    # check for field separator and quotes
                    char_locations: List[int] = [
                        match.start()
                        for match in re.finditer((re.escape(character)), field)
                    ]
                    for location in char_locations:
                        if any(
                            separator in field[location - 1]
                            for separator in separators
                        ):
                            raise UnsanitizedInputFound()
            return func(**kwargs)

        return wrapper

    return decorator


def validate_commit_hash(commit_hash: str) -> None:
    if not (
        # validate SHA-1
        re.match(
            r"^[A-Fa-f0-9]{40}$",
            commit_hash,
        )
        # validate SHA-256
        or re.match(
            r"^[A-Fa-f0-9]{64}$",
            commit_hash,
        )
    ):
        raise InvalidCommitHash()


def validate_commit_hash_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            commit_hash = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if not (
                # validate SHA-1
                re.match(
                    r"^[A-Fa-f0-9]{40}$",
                    commit_hash,
                )
                # validate SHA-256
                or re.match(
                    r"^[A-Fa-f0-9]{64}$",
                    commit_hash,
                )
            ):
                raise InvalidCommitHash()
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_int_range(
    value: int, lower_bound: int, upper_bound: int, inclusive: bool = True
) -> None:
    if inclusive:
        if not lower_bound <= value <= upper_bound:
            raise NumberOutOfRange(lower_bound, upper_bound, inclusive)
    else:
        if not lower_bound < value < upper_bound:
            raise NumberOutOfRange(lower_bound, upper_bound, inclusive)


def validate_int_range_deco(
    field: str, lower_bound: int, upper_bound: int, inclusive: bool
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            value = get_attr_value(field=field, kwargs=kwargs, obj_type=int)
            if inclusive:
                if not lower_bound <= value <= upper_bound:
                    raise NumberOutOfRange(lower_bound, upper_bound, inclusive)
            else:
                if not lower_bound < value < upper_bound:
                    raise NumberOutOfRange(lower_bound, upper_bound, inclusive)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_start_letter(value: str) -> None:
    if not value[0].isalpha():
        raise InvalidReportFilter("Password should start with a letter")


def validate_start_letter_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if not field_content[0].isalpha():
                raise InvalidReportFilter(
                    "Password should start with a letter"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_include_number(value: str) -> None:
    if not re.search(r"\d", value):
        raise InvalidReportFilter(
            "Password should include at least one number"
        )


def validate_include_number_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            print(field, field_content)
            if not re.search(r"\d", field_content):
                raise InvalidReportFilter(
                    "Password should include at least one number"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_include_lowercase(value: str) -> None:
    if not any(val.islower() for val in value):
        raise InvalidReportFilter(
            "Password should include lowercase characters"
        )


def validate_include_lowercase_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if not any(val.islower() for val in field_content):
                raise InvalidReportFilter(
                    "Password should include lowercase characters"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_include_uppercase(value: str) -> None:
    if not any(val.isupper() for val in value):
        raise InvalidReportFilter(
            "Password should include uppercase characters"
        )


def validate_include_uppercase_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            field_content = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if not any(val.isupper() for val in field_content):
                raise InvalidReportFilter(
                    "Password should include uppercase characters"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def sequence_increasing(
    char: str, current_ord: int, sequence: list[int], is_increasing: bool
) -> list[int]:
    if is_increasing and str(chr(sequence[-1])).isalnum() and char.isalnum():
        return [*sequence, current_ord]

    return [current_ord]


def sequence_decreasing(
    char: str, current_ord: int, sequence: list[int], is_increasing: bool
) -> list[int]:
    if (
        not is_increasing
        and str(chr(sequence[-1])).isalnum()
        and char.isalnum()
    ):
        return [*sequence, current_ord]

    return [current_ord]


def has_sequence(value: str, sequence_size: int = 3) -> bool:
    if len(value) < sequence_size or sequence_size <= 0:
        return False

    sequence: list[int] = [ord(value[0])]
    is_increasing = False
    for char in value[1:]:
        current_ord: int = ord(char)

        if sequence[-1] + 1 == current_ord:
            if len(sequence) == 1:
                is_increasing = True
            sequence = sequence_increasing(
                char, current_ord, sequence, is_increasing
            )
        elif sequence[-1] - 1 == current_ord:
            if len(sequence) == 1:
                is_increasing = False
            sequence = sequence_decreasing(
                char, current_ord, sequence, is_increasing
            )
        else:
            sequence = [current_ord]

        if len(sequence) == sequence_size:
            return True

    return False


def validate_sequence(value: str) -> None:
    if has_sequence(value):
        raise InvalidReportFilter(
            "Password should not include sequentials characters"
        )


def validate_sequence_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            value = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if has_sequence(value):
                raise InvalidReportFilter(
                    "Password should not include sequentials characters"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_symbols(value: str) -> None:
    if not re.search(r"[!\";#\$%&'\(\)\*\+,-./:<=>\?@\[\]^_`\{\|\}~]", value):
        raise InvalidReportFilter("Password should include symbols characters")


def validate_symbols_deco(field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            value = str(
                get_attr_value(field=field, kwargs=kwargs, obj_type=str)
            )
            if not re.search(
                r"[!\";#\$%&'\(\)\*\+,-./:<=>\?@\[\]^_`\{\|\}~]", value
            ):
                raise InvalidReportFilter(
                    "Password should include symbols characters"
                )
            return func(*args, **kwargs)

        return decorated

    return wrapper
