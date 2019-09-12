# -*- coding: utf-8 -*-

"""Fluid Asserts db module."""

# standard imports
from typing import List

# local imports
from fluidasserts import Unit, OPEN, CLOSED


def _get_result_as_tuple(*,
                         host: str, port: int,
                         msg_open: str, msg_closed: str,
                         vulns: List[str], safes: List[str]) -> tuple:
    """Return the tuple version of the Result object."""
    vuln_units: List[Unit] = []
    safe_units: List[Unit] = []

    if vulns:
        vuln_units.append(Unit(where=f'{host}:{port}',
                               specific=vulns))
    if safes:
        safe_units.append(Unit(where=f'{host}:{port}',
                               specific=safes))

    if vulns:
        return OPEN, msg_open, vuln_units, safe_units
    return CLOSED, msg_closed, vuln_units, safe_units
