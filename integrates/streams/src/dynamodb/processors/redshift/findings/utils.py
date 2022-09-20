# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from typing import (
    Any,
)


def format_row_metadata(
    item: dict[str, Any],
) -> dict[str, Any]:
    return dict(
        id=item["id"],
        cvss_version=item["cvss_version"],
        group_name=item["group_name"],
        hacker_email=item["analyst_email"],
        requirements=item["requirements"],
        sorts=item["sorts"],
        title=item["title"],
    )


def format_row_severity(
    item: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": item["id"],
        **item["severity"],
    }


def format_row_state(
    finding_id: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    return dict(
        id=finding_id,
        modified_by=state["modified_by"],
        modified_date=datetime.fromisoformat(state["modified_date"]),
        justification=state["justification"],
        source=state["source"],
        status=state["status"],
    )


def format_row_verification(
    finding_id: str,
    verification: dict[str, Any],
) -> dict[str, Any]:
    return dict(
        id=finding_id,
        modified_date=datetime.fromisoformat(verification["modified_date"]),
        status=verification["status"],
    )


def format_row_verification_vuln_ids(
    finding_id: str,
    modified_date: str,
    vulnerability_id: str,
) -> dict[str, Any]:
    return dict(
        id=finding_id,
        modified_date=datetime.fromisoformat(modified_date),
        vulnerability_id=vulnerability_id,
    )
