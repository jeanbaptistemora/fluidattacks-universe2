from api.schema import (
    SDL_CONTENT,
)
from datetime import (
    datetime,
)
import logging
import logging.config
from newutils import (
    datetime as date_utils,
)
from newutils.deprecations import (
    ApiDeprecation,
    get_deprecations_by_period,
)
import sys

LOGGER = logging.getLogger(__name__)


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
        fields += "".join(
            (
                f"{value} {field.field} of {parent} {key} was to be removed "
                f"in {date_utils.get_as_str(field.due_date, date_format)}\n"
            )
            for field in deprecated_fields
        )

    return base_output + fields


def lint_schema_deprecations(sdl_content: str) -> bool:
    """
    Parses the schema into an AST and returns `True` if it finds a field/value
    that should have been removed already, `False` otherwise.
    """
    yesterday: datetime = date_utils.get_now_minus_delta(days=1)
    (enums, operations) = get_deprecations_by_period(
        sdl_content=sdl_content, end=yesterday, start=None
    )
    if bool(enums):
        LOGGER.error(
            format_deprecation_output_log(enums, True),
            extra=dict(
                extra={
                    "overdue": enums.keys(),
                }
            ),
        )
    if bool(operations):
        LOGGER.error(
            format_deprecation_output_log(operations, False),
            extra=dict(
                extra={
                    "overdue": operations.keys(),
                }
            ),
        )

    return bool(enums) or bool(operations)


def main() -> None:
    failed_check: bool = lint_schema_deprecations(SDL_CONTENT)
    if failed_check:
        LOGGER.error("Failed check :(")
        sys.exit(1)
    LOGGER.info("No overdue deprecations found!")


if __name__ == "__main__":
    main()
