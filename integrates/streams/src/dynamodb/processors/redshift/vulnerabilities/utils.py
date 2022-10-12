# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)


def format_row_metadata(
    item: Item,
) -> Item:
    return dict(
        id=item.get("id") or str(item["pk"]).split("#")[1],
        custom_severity=item.get("custom_severity"),
        finding_id=item.get("finding_id") or str(item["sk"]).split("#")[1],
        skims_method=item.get("skims_method"),
        type=item["type"],
    )


def format_row_state(
    vulnerability_id: str,
    state: Item,
) -> Item:
    return dict(
        id=vulnerability_id,
        modified_by=state["modified_by"],
        modified_date=datetime.fromisoformat(state["modified_date"]),
        source=state["source"],
        status=state["status"],
    )


def format_row_treatment(
    vulnerability_id: str,
    treatment: Item,
) -> Item:
    return dict(
        id=vulnerability_id,
        modified_date=datetime.fromisoformat(treatment["modified_date"]),
        status=treatment["status"],
        accepted_until=datetime.fromisoformat(treatment["accepted_until"])
        if treatment.get("accepted_until")
        else None,
        acceptance_status=treatment.get("acceptance_status"),
    )


def format_row_verification(
    vulnerability_id: str,
    verification: Item,
) -> Item:
    return dict(
        id=vulnerability_id,
        modified_date=datetime.fromisoformat(verification["modified_date"]),
        status=verification["status"],
    )


def format_row_zero_risk(
    vulnerability_id: str,
    zero_risk: Item,
) -> Item:
    return dict(
        id=vulnerability_id,
        modified_date=datetime.fromisoformat(zero_risk["modified_date"]),
        status=zero_risk["status"],
    )
