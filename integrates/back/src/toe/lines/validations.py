from custom_exceptions import (
    InvalidLinesOfCode,
    InvalidModifiedDate,
    InvalidSortsRiskLevel,
    InvalidSortsRiskLevelDate,
    InvalidSortsSuggestions,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    SortsSuggestion,
)
import functools
from newutils import (
    datetime as datetime_utils,
)
from newutils.findings import (
    is_valid_finding_titles,
)
from newutils.validations import (
    get_attr_value,
)
from typing import (
    Any,
    Callable,
)


def validate_modified_date(modified_date: datetime) -> None:
    if modified_date > datetime_utils.get_now():
        raise InvalidModifiedDate()


def validate_modified_date_deco(modified_date_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            modified_date = get_attr_value(
                field=modified_date_field, kwargs=kwargs, obj_type=datetime
            )
            if modified_date > datetime_utils.get_now():
                raise InvalidModifiedDate()
            res = func(*args, **kwargs)
            return res

        return decorated

    return wrapper


def validate_loc(loc: int) -> None:
    if loc < 0:
        raise InvalidLinesOfCode()


def validate_loc_deco(loc_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            loc = get_attr_value(field=loc_field, kwargs=kwargs, obj_type=int)
            if loc < 0:
                raise InvalidLinesOfCode()
            res = func(*args, **kwargs)
            return res

        return decorated

    return wrapper


def validate_sort_risk_level(value: int) -> None:
    if not 0 <= value <= 100:
        raise InvalidSortsRiskLevel.new()


def validate_sort_risk_level_deco(value_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            value: int = get_attr_value(
                field=value_field, kwargs=kwargs, obj_type=int
            )
            if not 0 <= value <= 100:
                raise InvalidSortsRiskLevel.new()
            res = func(*args, **kwargs)
            return res

        return decorated

    return wrapper


def validate_sorts_risk_level_date(sorts_risk_level_date: datetime) -> None:
    if sorts_risk_level_date > datetime.today():
        raise InvalidSortsRiskLevelDate()


def validate_sorts_risk_level_date_deco(
    sorts_risk_level_date_field: str,
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            sorts_risk_level_date: datetime = get_attr_value(
                field=sorts_risk_level_date_field,
                kwargs=kwargs,
                obj_type=datetime,
            )
            if sorts_risk_level_date > datetime.today():
                raise InvalidSortsRiskLevelDate()
            res = func(*args, **kwargs)
            return res

        return decorated

    return wrapper


async def validate_sort_suggestions(
    loaders: Dataloaders,
    suggestions: list[SortsSuggestion],
) -> None:
    if len(suggestions) > 5:
        raise InvalidSortsSuggestions.new()
    await is_valid_finding_titles(
        loaders, [item.finding_title for item in suggestions]
    )
    for item in suggestions:
        if not 0 <= item.probability <= 100:
            raise InvalidSortsSuggestions.new()
