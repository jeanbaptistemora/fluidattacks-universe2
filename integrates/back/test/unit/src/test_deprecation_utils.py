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
from freezegun import (  # type: ignore
    freeze_time,
)
from newutils.datetime import (
    get_from_str,
    get_now,
    get_now_minus_delta,
    get_now_plus_delta,
)
from newutils.deprecations import (
    ApiDeprecation,
    filter_api_deprecation_list,
    get_deprecations_by_period,
    get_due_date,
)
import os
import pytest

MOCK_SCHEMA_PATH: str = os.path.dirname(os.path.abspath(__file__))
MOCK_SDL_CONTENT: str = load_schema_from_path(MOCK_SCHEMA_PATH)


def test_get_deprecations_by_period() -> None:
    # Without a start date
    deprecations = get_deprecations_by_period(
        sdl_content=MOCK_SDL_CONTENT, end=get_now(), start=None
    )
    expected_fields: list[str] = [
        "OLD_VALUE",
        "deprecatedField",
        "deprecatedName",
        "deprecatedInput",
        "deprecatedArg",
    ]
    deprecation_values: list[str] = [
        deprecation.field
        for deprecated_fields in deprecations.values()
        for deprecation in deprecated_fields
    ]
    assert Counter(deprecation_values) == Counter(expected_fields)

    # With a start date not very close to the deprecation dates
    no_deprecations = get_deprecations_by_period(
        sdl_content=MOCK_SDL_CONTENT,
        end=get_now(),
        start=get_now_minus_delta(days=30),
    )
    assert no_deprecations == {}


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


@freeze_time("2020-06-01")
def test_filter_api_deprecation_list() -> None:
    deprecations: list[ApiDeprecation] = [
        ApiDeprecation(
            parent="testParent",
            field="deprecatedField",
            reason="This field will be removed in 2020/01/01",
            due_date=get_from_str("2020/01/01", "%Y/%m/%d"),
            type="object_type_definition",
        ),
        ApiDeprecation(
            parent="testParent2",
            field="deprecatedField2",
            reason="This field will be removed in 2020/02/15",
            due_date=get_from_str("2020/02/15", "%Y/%m/%d"),
            type="object_type_definition",
        ),
        ApiDeprecation(
            parent="customDirective",
            field="deprecatedDirectiveField",
            reason="This field will be removed in 2020/06/15",
            due_date=get_from_str("2020/06/15", "%Y/%m/%d"),
            type="directive_definition",
        ),
    ]
    assert (
        len(
            filter_api_deprecation_list(
                deprecations=deprecations,
                end=get_now_plus_delta(days=15),
                start=None,
            )
        )
        == 3
    )
    assert (
        len(
            filter_api_deprecation_list(
                deprecations=deprecations, end=get_now(), start=None
            )
        )
        == 2
    )
    assert (
        len(
            filter_api_deprecation_list(
                deprecations=deprecations,
                end=get_now(),
                start=get_now_minus_delta(days=30),
            )
        )
        == 0
    )
