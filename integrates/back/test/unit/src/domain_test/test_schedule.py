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
    report_date: date = datetime_utils.get_now_minus_delta(days=1).date()
    in_range_date: date = datetime_utils.get_now_minus_delta(days=2).date()
    in_range_date2: date = datetime_utils.get_now_minus_delta(days=9).date()
    assert _validate_date(report_date, 1, 0)
    assert _validate_date(in_range_date, 2, 1)
    assert _validate_date(in_range_date, 9, 1)
    assert _validate_date(in_range_date2, 9, 1)


def test_validate_date_fail() -> None:
    actual_date: date = datetime_utils.get_now().date()
    not_in_range_date: date = datetime_utils.get_now_minus_delta(days=2).date()
    not_in_range_date2: date = datetime_utils.get_now_minus_delta(
        days=10
    ).date()
    assert not _validate_date(actual_date, 1, 0)
    assert not _validate_date(actual_date, 9, 2)
    assert not _validate_date(not_in_range_date, 1, 0)
    assert not _validate_date(not_in_range_date, 9, 2)
    assert not _validate_date(not_in_range_date2, 9, 0)
    assert not _validate_date(not_in_range_date2, 20, 10)


@pytest.mark.parametrize(
    [
        "content",
        "user_email",
    ],
    [
        [
            {
                "test@test.com": {
                    "enumerated": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "verified": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "loc": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "reattacked": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "groups": {
                        "unittesting": {
                            "verified": 0,
                            "enumerated": 0,
                            "loc": 0,
                        },
                        "test_group": {
                            "verified": 0,
                            "enumerated": 0,
                            "loc": 0,
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
    date_days = 3 if datetime_utils.get_now().weekday() == 0 else 1

    fields: List[str] = [
        "verified",
        "verified",
        "verified",
        "enumerated",
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
            date_range=date_days,
            date_report=datetime_utils.get_now_minus_delta(days=date_days),
            field=field,
            group=group,
            user_email=user_email,
        )

    assert content[user_email]["verified"]["count"]["today"] == 3
    assert content[user_email]["enumerated"]["count"]["today"] == 1
    assert content[user_email]["groups"]["unittesting"]["enumerated"] == 1
    assert content[user_email]["groups"]["unittesting"]["verified"] == 2
    assert content[user_email]["groups"]["test_group"]["verified"] == 1
    content = _generate_count_report(
        content=content,
        date_range=date_days,
        date_report=datetime_utils.get_now_minus_delta(days=date_days + 1),
        field="verified",
        group="test_group",
        user_email=user_email,
    )
    content = _generate_count_report(
        content=content,
        date_range=date_days,
        date_report=datetime_utils.get_now_minus_delta(days=date_days + 1),
        field="verified",
        group="test_group",
        user_email=user_email,
    )
    assert content[user_email]["verified"]["count"]["past_day"] == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        [
            {
                "enumerated": {
                    "count": {
                        "past_day": 4,
                        "today": 10,
                    }
                },
                "verified": {
                    "count": {
                        "past_day": 3,
                        "today": 5,
                    }
                },
                "loc": {
                    "count": {
                        "past_day": 0,
                        "today": 0,
                    }
                },
                "reattacked": {
                    "count": {
                        "past_day": 0,
                        "today": 0,
                    }
                },
                "groups": {
                    "unittesting": {
                        "verified": 6,
                        "enumerated": 3,
                        "loc": 0,
                    },
                    "test_group": {
                        "verified": 4,
                        "enumerated": 2,
                        "loc": 0,
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
