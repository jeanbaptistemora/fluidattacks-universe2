from dataloaders import (
    get_new_context,
)
from datetime import (
    date,
    datetime,
)
from newutils import (
    datetime as datetime_utils,
)
import pytest
from schedulers.numerator_report_digest import (
    _common_generate_count_report,
    _send_mail_report,
    _validate_date,
    get_percent,
)
from typing import (
    Any,
)
from unittest import (
    mock,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_get_percent() -> None:
    assert get_percent(0, 10) == "+0%"
    assert get_percent(10, 0) == "-"
    # FP: local testing
    assert get_percent("0", 10) == "-"  # type: ignore  # NOSONAR
    assert get_percent(-10, 10) == "-100%"
    assert get_percent(0.55, 10) == "+6%"
    assert get_percent(2, 3) == "+67%"
    assert get_percent(3, 2) == "+150%"
    assert get_percent(-2, 3) == "-67%"
    assert get_percent(-3, 2) == "-150%"


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
                    "enumerated_inputs": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "enumerated_ports": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "verified_inputs": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "verified_ports": {
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
                    "released": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "evidences": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "draft_created": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "draft_rejected": {
                        "count": {
                            "past_day": 0,
                            "today": 0,
                        }
                    },
                    "max_cvss": 0.0,
                    "oldest_draft": 0,
                    "groups": {
                        "unittesting": {
                            "verified_inputs": 0,
                            "verified_ports": 0,
                            "enumerated_inputs": 0,
                            "enumerated_ports": 0,
                            "loc": 0,
                            "reattacked": 0,
                            "released": 0,
                            "evidences": 0,
                            "draft_created": 0,
                            "draft_rejected": 0,
                        },
                        "test_group": {
                            "verified_inputs": 0,
                            "verified_ports": 0,
                            "enumerated_inputs": 0,
                            "enumerated_ports": 0,
                            "loc": 0,
                            "reattacked": 0,
                            "released": 0,
                            "evidences": 0,
                            "draft_created": 0,
                            "draft_rejected": 0,
                        },
                    },
                },
            },
            "test@test.com",
        ],
    ],
)
def test_common_generate_count_report(
    *,
    content: dict[str, Any],
    user_email: str,
) -> None:
    date_days = 3 if datetime_utils.get_now().weekday() == 0 else 1

    fields: list[str] = [
        "verified_inputs",
        "verified_inputs",
        "verified_inputs",
        "verified_ports",
        "verified_ports",
        "enumerated_inputs",
        "enumerated_ports",
        "enumerated_ports",
        "released",
        "evidences",
    ]
    groups: list[str] = [
        "unittesting",
        "unittesting",
        "test_group",
        "test_group",
        "unittesting",
        "unittesting",
        "test_group",
        "unittesting",
        "test_group",
    ]

    for group, field in zip(groups, fields):
        _common_generate_count_report(
            content=content,
            date_range=date_days,
            date_report=datetime_utils.get_now_minus_delta(days=date_days),
            field=field,
            group=group,
            user_email=user_email,
            allowed_users=["test@test.com"],
        )

    assert content[user_email]["verified_inputs"]["count"]["today"] == 3
    assert content[user_email]["enumerated_inputs"]["count"]["today"] == 1
    assert content[user_email]["released"]["count"]["today"] == 1
    assert content[user_email]["evidences"]["count"]["today"] == 0
    assert (
        content[user_email]["groups"]["unittesting"]["enumerated_inputs"] == 1
    )
    assert (
        content[user_email]["groups"]["unittesting"]["enumerated_ports"] == 1
    )
    assert content[user_email]["groups"]["unittesting"]["verified_inputs"] == 2
    assert content[user_email]["groups"]["unittesting"]["verified_ports"] == 1
    assert (
        content[user_email]["groups"]["test_group"]["enumerated_inputs"] == 0
    )
    assert content[user_email]["groups"]["test_group"]["enumerated_ports"] == 1
    assert content[user_email]["groups"]["test_group"]["verified_inputs"] == 1
    assert content[user_email]["groups"]["test_group"]["verified_ports"] == 1
    assert content[user_email]["groups"]["test_group"]["released"] == 1
    assert content[user_email]["groups"]["test_group"]["evidences"] == 0
    past_days = 4 if datetime_utils.get_now().weekday() == 1 else date_days + 1
    _common_generate_count_report(
        content=content,
        date_range=date_days,
        date_report=datetime_utils.get_now_minus_delta(days=past_days),
        field="verified_inputs",
        group="test_group",
        user_email=user_email,
        allowed_users=["test@test.com"],
    )
    _common_generate_count_report(
        content=content,
        date_range=date_days,
        date_report=datetime_utils.get_now_minus_delta(days=past_days),
        field="verified_inputs",
        group="test_group",
        user_email=user_email,
        allowed_users=["test@test.com"],
    )
    assert content[user_email]["verified_inputs"]["count"]["past_day"] == 2
    _common_generate_count_report(
        content=content,
        date_range=date_days,
        date_report=datetime_utils.get_now_minus_delta(days=past_days),
        field="verified_ports",
        group="test_group",
        user_email=user_email,
        allowed_users=["test@test.com"],
    )
    _common_generate_count_report(
        content=content,
        date_range=date_days,
        date_report=datetime_utils.get_now_minus_delta(days=past_days),
        field="verified_ports",
        group="test_group",
        user_email=user_email,
        allowed_users=["test@test.com"],
    )
    assert content[user_email]["verified_ports"]["count"]["past_day"] == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        [
            {
                "enumerated_inputs": {
                    "count": {
                        "past_day": 4,
                        "today": 10,
                    }
                },
                "verified_inputs": {
                    "count": {
                        "past_day": 3,
                        "today": 5,
                    }
                },
                "enumerated_ports": {
                    "count": {
                        "past_day": 4,
                        "today": 10,
                    }
                },
                "verified_ports": {
                    "count": {
                        "past_day": 3,
                        "today": 5,
                    }
                },
                "loc": {
                    "count": {
                        "past_day": 4,
                        "today": 5,
                    }
                },
                "reattacked": {
                    "count": {
                        "past_day": 3,
                        "today": 2,
                    }
                },
                "released": {
                    "count": {
                        "past_day": 1,
                        "today": 2,
                    }
                },
                "evidences": {
                    "count": {
                        "past_day": 1,
                        "today": 2,
                    }
                },
                "draft_created": {
                    "count": {
                        "past_day": 0,
                        "today": 0,
                    }
                },
                "draft_rejected": {
                    "count": {
                        "past_day": 0,
                        "today": 0,
                    }
                },
                "max_cvss": 0.0,
                "oldest_draft": 0,
                "groups": {
                    "unittesting": {
                        "verified_inputs": 6,
                        "verified_ports": 6,
                        "enumerated_inputs": 3,
                        "enumerated_ports": 3,
                        "loc": 0,
                    },
                    "test_group": {
                        "verified_inputs": 4,
                        "verified_ports": 4,
                        "enumerated_inputs": 2,
                        "enumerated_ports": 2,
                        "loc": 0,
                    },
                },
            },
        ],
    ],
)
async def test_send_mail_numerator_report(
    content: dict[str, Any],
) -> None:
    with mock.patch(
        "schedulers.numerator_report_digest.mail_numerator_report",
        new_callable=mock.AsyncMock,
    ) as mock_mail_numerator_report:
        mock_mail_numerator_report.return_value = True
        await _send_mail_report(
            loaders=get_new_context(),
            content=content,
            report_date=datetime.fromisoformat(
                "2022-07-08T06:00:00+00:00"
            ).date(),
            responsible="integratesmanager@gmail.com",
        )
    assert mock_mail_numerator_report.called is True
