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


def adjust_historic_dates(
    historic: tuple[Any, ...],
) -> tuple[Any, ...]:
    """
    Ensure dates are not the same and in ascending order.
    Also add a minimum 1 second offset among them.
    """
    if not historic:
        return tuple()
    new_historic = [historic[0]]
    base_date = historic[0].modified_date
    for entry in historic[1:]:
        base_date = get_date_with_offset(base_date, entry.modified_date)
        new_historic.append(entry._replace(modified_date=base_date))

    return tuple(new_historic)


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


def get_date_with_offset(
    base_iso8601: str, target_iso8601: str, offset: int = 1
) -> str:
    """Guarantee at least n seconds separation between dates."""
    max_date = max(
        datetime.fromisoformat(base_iso8601) + timedelta(seconds=offset),
        datetime.fromisoformat(target_iso8601),
    )
    return max_date.astimezone(tz=timezone.utc).isoformat()


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
