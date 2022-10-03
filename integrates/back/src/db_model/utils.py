# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model.types import (
    PoliciesToUpdate,
)
from decimal import (
    Decimal,
)
from typing import (
    Any,
)


def get_date_as_utc_iso_format(date: datetime) -> str:
    return date.astimezone(tz=timezone.utc).isoformat()


def get_min_iso_date(date: datetime) -> datetime:
    return datetime.combine(
        date.astimezone(tz=timezone.utc),
        datetime.min.time(),
    )


def get_first_day_iso_date() -> str:
    now = get_min_iso_date(datetime.now(tz=timezone.utc))

    return (now - timedelta(days=(now.isoweekday() - 1) % 7)).isoformat()


def format_policies_to_update(
    policies_data: dict[str, Any],
) -> PoliciesToUpdate:
    return PoliciesToUpdate(
        max_acceptance_days=int(policies_data["max_acceptance_days"])
        if policies_data.get("max_acceptance_days") is not None
        else None,
        max_acceptance_severity=Decimal(
            policies_data["max_acceptance_severity"]
        ).quantize(Decimal("0.1"))
        if policies_data.get("max_acceptance_severity") is not None
        else None,
        max_number_acceptances=int(policies_data["max_number_acceptances"])
        if policies_data.get("max_number_acceptances") is not None
        else None,
        min_acceptance_severity=Decimal(
            policies_data["min_acceptance_severity"]
        ).quantize(Decimal("0.1"))
        if policies_data.get("min_acceptance_severity") is not None
        else None,
        min_breaking_severity=Decimal(
            policies_data["min_breaking_severity"]
        ).quantize(Decimal("0.1"))
        if policies_data.get("min_breaking_severity") is not None
        else None,
        vulnerability_grace_period=int(
            policies_data["vulnerability_grace_period"]
        )
        if policies_data.get("vulnerability_grace_period") is not None
        else None,
    )
