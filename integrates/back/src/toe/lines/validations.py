from custom_exceptions import (
    InvalidLinesOfCode,
    InvalidModifiedDate,
    InvalidSortsRiskLevel,
    InvalidSortsSuggestions,
)
from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    SortsSuggestion,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.findings import (
    is_valid_finding_titles,
)


def validate_modified_date(modified_date: datetime) -> None:
    if modified_date > datetime_utils.get_now():
        raise InvalidModifiedDate()


def validate_loc(loc: int) -> None:
    if loc < 0:
        raise InvalidLinesOfCode()


def validate_sort_risk_level(value: int) -> None:
    if not 0 <= value <= 100:
        raise InvalidSortsRiskLevel.new()


async def validate_sort_suggestions(
    suggestions: list[SortsSuggestion],
) -> None:
    if len(suggestions) > 5:
        raise InvalidSortsSuggestions.new()
    await is_valid_finding_titles([item.finding_title for item in suggestions])
    for item in suggestions:
        if not 0 <= item.probability <= 100:
            raise InvalidSortsSuggestions.new()
