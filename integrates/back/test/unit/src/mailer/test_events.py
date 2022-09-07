# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=too-many-arguments
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from mailer.events import (
    send_mail_event_report,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "group_name",
        "event_id",
        "event_type",
        "description",
        "root_id",
        "reason",
        "other",
        "is_closed",
    ],
    [
        [
            "unittesting",
            "538745942",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "Test",
            "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            None,
            None,
            False,
        ],
        [
            "unittesting",
            "538745942",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "Test",
            "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            "PROBLEM_SOLVED",
            None,
            True,
        ],
        [
            "unittesting",
            "538745942",
            "AUTHORIZATION_SPECIAL_ATTACK",
            "Test",
            "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            "OTHER",
            "Test",
            True,
        ],
    ],
)
async def test_send_event_report(
    group_name: str,
    event_id: str,
    event_type: str,
    description: str,
    reason: str,
    root_id: str,
    other: str,
    is_closed: bool,
) -> None:
    await send_mail_event_report(
        loaders=get_new_context(),
        group_name=group_name,
        event_id=event_id,
        event_type=event_type,
        description=description,
        root_id=root_id,
        reason=reason,
        other=other,
        is_closed=is_closed,
        report_date=datetime(2022, 6, 16).date(),
    )
