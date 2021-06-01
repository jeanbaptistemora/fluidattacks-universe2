# -*- coding: utf-8 -*-

"""Fluid Asserts GCP cloud package."""


from fluidasserts import (
    CLOSED,
    OPEN,
    Unit,
)
from typing import (
    List,
)


def _get_result_as_tuple(
    *,
    service: str,
    objects: str,
    msg_open: str,
    msg_closed: str,
    vulns: List[str],
    safes: List[str],
) -> tuple:
    """Return the tuple version of the Result object."""
    vuln_units: List[Unit] = []
    safe_units: List[Unit] = []

    if vulns:
        vuln_units.extend(
            Unit(where=f"GCP/{service}/{id_}", specific=[vuln])
            for id_, vuln in vulns
        )
    if safes:
        safe_units.extend(
            Unit(where=f"GCP/{service}/{id_}", specific=[safe])
            for id_, safe in safes
        )

    if vulns:
        return OPEN, msg_open, vuln_units, safe_units
    if safes:
        return CLOSED, msg_closed, vuln_units, safe_units
    return CLOSED, f"No {objects} found to check", vuln_units, safe_units
