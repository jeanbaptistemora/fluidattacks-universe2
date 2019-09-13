# -*- coding: utf-8 -*-

"""Fluid Asserts AWS cloud package."""

# standard imports
from typing import List

# local imports
from fluidasserts import Unit, OPEN, CLOSED


def _get_result_as_tuple(*,
                         service: str, objects: str,
                         msg_open: str, msg_closed: str,
                         vulns: List[str], safes: List[str]) -> tuple:
    """Return the tuple version of the Result object."""
    vuln_units: List[Unit] = []
    safe_units: List[Unit] = []

    if vulns:
        vuln_units.append(Unit(where=f'AWS/{service}',
                               specific=vulns))
    if safes:
        safe_units.append(Unit(where=f'AWS/{service}',
                               specific=safes))

    if vulns:
        return OPEN, msg_open, vuln_units, safe_units
    if safes:
        return CLOSED, msg_closed, vuln_units, safe_units
    return CLOSED, f'No {objects} found to check', vuln_units, safe_units
