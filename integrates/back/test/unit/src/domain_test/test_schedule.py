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
    _generate_count_report,
    _send_mail_report,
    _validate_date,
    get_variation,
)
from typing import (
    Any,
    Dict,
    List,
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


@pytest.mark.parametrize(
    [
        "content",
        "user_email",
    ],
    [
        [
            {
                "test@test.com": {
                    "past_day_enumerated_count": 0,
                    "past_day_verified_count": 0,
                    "today_enumerated_count": 0,
                    "today_verified_count": 0,
                    "groups": {
                        "unittesting": {
                            "verified_count": 0,
                            "enumerated_count": 0,
                        },
                        "test_group": {
                            "verified_count": 0,
                            "enumerated_count": 0,
                        },
                    },
                },
            },
            "test@test.com",
        ],
    ],
)
def test_generate_count_report(
    *,
    content: Dict[str, Any],
    user_email: str,
) -> None:
    fields: List[str] = [
        "verified_count",
        "verified_count",
        "verified_count",
        "enumerated_count",
    ]
    groups: List[str] = [
        "unittesting",
        "unittesting",
        "test_group",
        "unittesting",
    ]

    for group, field in zip(groups, fields):
        content = _generate_count_report(
            content=content,
            date_report=datetime_utils.get_now(),
            field=field,
            group=group,
            user_email=user_email,
        )

    assert content[user_email]["today_verified_count"] == 3
    assert content[user_email]["today_enumerated_count"] == 1
    assert (
        content[user_email]["groups"]["unittesting"]["enumerated_count"] == 1
    )
    assert content[user_email]["groups"]["unittesting"]["verified_count"] == 2
    assert content[user_email]["groups"]["test_group"]["verified_count"] == 1
    content = _generate_count_report(
        content=content,
        date_report=datetime_utils.get_now_minus_delta(days=1),
        field="verified_count",
        group="test_group",
        user_email=user_email,
    )
    content = _generate_count_report(
        content=content,
        date_report=datetime_utils.get_now_minus_delta(days=1),
        field="verified_count",
        group="test_group",
        user_email=user_email,
    )
    assert content[user_email]["past_day_verified_count"] == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        [
            {
                "past_day_enumerated_count": 4,
                "past_day_verified_count": 3,
                "today_enumerated_count": 10,
                "today_verified_count": 5,
                "groups": {
                    "unittesting": {
                        "verified_count": 6,
                        "enumerated_count": 3,
                    },
                    "test_group": {
                        "verified_count": 4,
                        "enumerated_count": 2,
                    },
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
