from api.schema import (
    SDL_CONTENT,
)
from api.utils.ast import (
    get_deprecations_by_period,
)
from api.utils.types import (
    ApiDeprecation,
)
from datetime import (
    datetime,
)
from newutils import (
    datetime as date_utils,
)


def format_deprecation_output_log(
    deprecations: dict[str, list[ApiDeprecation]], is_enum: bool
) -> str:
    """
    Translates the deprecation dicts to a more readable logging format that
    looks like:

    `Found overdue deprecated fields:`

    `Field isDeprecated of parent importantQuery was deprecated in 1999/01/01`
    """
    date_format: str = "%Y/%m/%d"
    value: str = "Value" if is_enum else "Field"
    parent: str = "enum" if is_enum else "parent"
    base_output: str = f"Found overdue deprecated {value.lower()}s:\n\n"
    fields: str = ""
    for key, deprecated_fields in deprecations.items():
        fields += "\n".join(
            f"""{value} {field.field} of {parent} {key} was deprecated in
            {date_utils.get_as_str(field.due_date, date_format)}"""
            for field in deprecated_fields
        )

    return base_output + fields


def lint_schema_deprecations() -> None:
    yesterday: datetime = date_utils.get_now_minus_delta(days=1)
    (enums, operations) = get_deprecations_by_period(
        sdl_content=SDL_CONTENT, end=yesterday, start=None
    )
    if len(enums.keys()) > 0:
        print(format_deprecation_output_log(enums, True))
    if len(operations.keys()) > 0:
        print(format_deprecation_output_log(operations, False))


def main() -> None:
    lint_schema_deprecations()
