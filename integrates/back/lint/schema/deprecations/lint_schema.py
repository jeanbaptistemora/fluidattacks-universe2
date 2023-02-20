from api import (
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
    ApiFieldType,
    get_deprecations_by_period,
)
import sys

LOGGER = logging.getLogger(__name__)


def format_deprecation_output_log(
    deprecations: dict[str, list[ApiDeprecation]]
) -> str:
    """
    Translates the deprecation dicts to a more readable logging format that
    looks like:

    `Found overdue deprecated fields:`

    `Field isDeprecated of parent importantQuery was deprecated in 1999/01/01`
    """
    base_output: str = "Found overdue deprecated fields:\n\n"
    fields: str = ""
    for key, deprecated_fields in deprecations.items():
        fields += "".join(
            (
                f"{'Value' if field.type == ApiFieldType.ENUM else 'Field'} "
                f"{field.field} of "
                f"{'enum' if field.type == ApiFieldType.ENUM else 'parent'} "
                f"{key} was to be removed in "
                f"{date_utils.get_as_str(field.due_date, '%Y/%m/%d')}\n"
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
    deprecations: dict[str, list[ApiDeprecation]] = get_deprecations_by_period(
        sdl_content=sdl_content, end=yesterday, start=None
    )
    if has_deprecations := bool(deprecations):
        LOGGER.error(
            format_deprecation_output_log(deprecations),
            extra=dict(
                extra={
                    "overdue": deprecations.keys(),
                }
            ),
        )

    return has_deprecations


def main() -> None:
    failed_check: bool = lint_schema_deprecations(SDL_CONTENT)
    if failed_check:
        LOGGER.error("Failed check :(")
        sys.exit(1)
    LOGGER.info("No overdue deprecations found!")


if __name__ == "__main__":
    main()
