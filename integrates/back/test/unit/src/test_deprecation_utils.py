from ariadne import (
    load_schema_from_path,
)
from collections import (
    Counter,
)
from custom_exceptions import (
    InvalidDateFormat,
)
from datetime import (
    datetime,
)
from newutils.datetime import (
    get_from_str,
    get_now,
    get_now_minus_delta,
)
from newutils.deprecations.ast import (
    get_deprecations_by_period,
    get_due_date,
)
import os
import pytest

MOCK_SCHEMA_PATH: str = os.path.dirname(os.path.abspath(__file__))
MOCK_SDL_CONTENT: str = load_schema_from_path(MOCK_SCHEMA_PATH)


def test_get_deprecations_by_period() -> None:
    enums, operations = get_deprecations_by_period(
        sdl_content=MOCK_SDL_CONTENT, end=get_now(), start=None
    )
    expected_fields: list[str] = [
        "OLD_VALUE",
        "deprecatedField",
        "deprecatedName",
        "deprecatedInput",
        "deprecatedArg",
    ]
    enum_values: list[str] = [
        deprecation.field
        for deprecations in enums.values()
        for deprecation in deprecations
    ]
    operation_values: list[str] = [
        deprecation.field
        for deprecations in operations.values()
        for deprecation in deprecations
    ]
    assert Counter(enum_values + operation_values) == Counter(expected_fields)

    no_enums, no_operations = get_deprecations_by_period(
        sdl_content=MOCK_SDL_CONTENT,
        end=get_now(),
        start=get_now_minus_delta(days=30),
    )
    assert no_enums == no_operations == {}


def test_get_due_date() -> None:
    due_date: datetime = get_due_date(
        definition="TestDefinition",
        field="deprecatedField",
        reason="This field will be removed in 2020/01/01",
    )
    assert due_date == get_from_str("2020/01/01", "%Y/%m/%d")

    # No date
    with pytest.raises(InvalidDateFormat):
        get_due_date(
            definition="TestDefinition",
            field="deprecatedField",
            reason="This reason field does not have a date :(",
        )
    # DD/MM/YYYY or MM/DD/YYYY
    with pytest.raises(InvalidDateFormat):
        get_due_date(
            definition="TestDefinition",
            field="deprecatedField",
            reason="This reason field has a badly formatted date 01/01/2020",
        )
