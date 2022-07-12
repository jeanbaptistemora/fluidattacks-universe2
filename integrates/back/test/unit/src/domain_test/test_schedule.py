from dataloaders import (
    get_new_context,
)
from datetime import (
    date,
)
from newutils import (
    datetime as datetime_utils,
)
import pytest
from schedulers.numerator_report_digest import (
    _send_mail_report,
    _validate_date,
    get_variation,
)
from typing import (
    Any,
    Dict,
)


def test_get_variation() -> None:
    assert get_variation(10, 10) == "0.0%"
    assert get_variation(0, 10) == "N/A"
    assert get_variation("0", 10) == "N/A"
    assert get_variation(10, 0) == "-100.0%"
    assert get_variation(10, 10.555) == "5.55%"


def test_validate_date() -> None:
    actual_date: date = datetime_utils.get_now().date()
    in_range_date: date = datetime_utils.get_now_minus_delta(days=1).date()
    in_range_date2: date = datetime_utils.get_now_minus_delta(days=8).date()
    assert _validate_date(actual_date, 1, 0)
    assert _validate_date(in_range_date, 2, 1)
    assert _validate_date(in_range_date, 9, 1)
    assert _validate_date(in_range_date2, 9, 1)


def test_validate_date_fail() -> None:
    actual_date: date = datetime_utils.get_now().date()
    not_in_range_date: date = datetime_utils.get_now_minus_delta(days=1).date()
    not_in_range_date2: date = datetime_utils.get_now_minus_delta(
        days=9
    ).date()
    assert not _validate_date(actual_date, 2, 1)
    assert not _validate_date(actual_date, 9, 1)
    assert not _validate_date(not_in_range_date, 1, 0)
    assert not _validate_date(not_in_range_date, 9, 2)
    assert not _validate_date(not_in_range_date2, 1, 0)
    assert not _validate_date(not_in_range_date2, 9, 1)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        [
            {
                "weekly_count": 10,
                "past_day_count": 5,
                "today_count": 4,
                "groups": {
                    "unittesting": 2,
                    "test_group": 2,
                },
            },
        ],
    ],
)
async def test_send_mail_numerator_report(
    content: Dict[str, Any],
) -> None:
    await _send_mail_report(
        loaders=get_new_context(),
        content=content,
        report_date="2022-07-08T06:00:00+00:00",
        responsible="integratesmanager@gmail.com",
    )
