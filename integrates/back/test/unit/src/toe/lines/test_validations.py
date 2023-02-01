from custom_exceptions import (
    InvalidLinesOfCode,
    InvalidModifiedDate,
    InvalidSortsRiskLevelDate,
    InvalidSortsSuggestions,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.toe_lines.types import (
    SortsSuggestion,
)
from newutils import (
    datetime as datetime_utils,
)
import pytest
from toe.lines.validations import (
    validate_loc,
    validate_loc_deco,
    validate_modified_date,
    validate_modified_date_deco,
    validate_sort_suggestions,
    validate_sorts_risk_level_date,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_modified_date() -> None:
    modified_date = datetime_utils.get_now() - timedelta(days=1)
    modified_date_fail = datetime_utils.get_now() + timedelta(days=1)
    validate_modified_date(modified_date)
    with pytest.raises(InvalidModifiedDate):
        validate_modified_date(modified_date_fail)


def test_validate_modified_date_deco() -> None:
    @validate_modified_date_deco("modified_date")
    def decorated_func(modified_date: str) -> str:
        return modified_date

    modified_date = datetime_utils.get_now() - timedelta(days=1)
    modified_date_fail = datetime_utils.get_now() + timedelta(days=1)
    decorated_func(modified_date=modified_date)
    with pytest.raises(InvalidModifiedDate):
        decorated_func(modified_date=modified_date_fail)


def test_validate_loc() -> None:
    validate_loc(loc=4)
    with pytest.raises(InvalidLinesOfCode):
        validate_loc(loc=-4)


def test_validate_loc_deco() -> None:
    @validate_loc_deco(loc_field="loc")
    def decorated_func(loc: int) -> int:
        return loc

    decorated_func(loc=4)
    with pytest.raises(InvalidLinesOfCode):
        decorated_func(loc=-4)


def test_validate_sorts_risk_level_date() -> None:
    modified_date = datetime.now() - timedelta(days=1)
    modified_date_fail = datetime.now() + timedelta(days=1)
    validate_sorts_risk_level_date(modified_date)
    with pytest.raises(InvalidSortsRiskLevelDate):
        validate_sorts_risk_level_date(modified_date_fail)


async def test_valid_suggestions() -> None:
    await validate_sort_suggestions(
        [
            SortsSuggestion(
                "366. Inappropriate coding practices - Transparency Conflict",
                50,
            ),
        ]
    )
    with pytest.raises(InvalidSortsSuggestions):
        await validate_sort_suggestions(
            [
                SortsSuggestion(
                    "060. Insecure service configuration - Host verification",
                    150,
                ),
            ]
        )
    with pytest.raises(InvalidSortsSuggestions):
        await validate_sort_suggestions(
            [
                SortsSuggestion(
                    "060. Insecure service configuration - Host verification",
                    50,
                ),
                SortsSuggestion(
                    "060. Insecure service configuration - Host verification",
                    60,
                ),
                SortsSuggestion(
                    "428. Inappropriate coding practices - invalid file", 70
                ),
                SortsSuggestion(
                    "428. Inappropriate coding practices - invalid file", 10
                ),
                SortsSuggestion(
                    "428. Inappropriate coding practices - invalid file", 10
                ),
                SortsSuggestion(
                    "428. Inappropriate coding practices - invalid file", 10
                ),
            ]
        )
