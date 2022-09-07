# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Fluid Asserts db module."""


from fluidasserts import (
    CLOSED,
    OPEN,
    Unit,
)
import inspect
from typing import (
    List,
)


def _get_result_as_tuple(
    *,
    host: str,
    port: int,
    msg_open: str,
    msg_closed: str,
    vulns: List[str],
    safes: List[str],
) -> tuple:
    """Return the tuple version of the Result object."""
    vuln_units: List[Unit] = []
    safe_units: List[Unit] = []
    frm = inspect.stack()
    database = inspect.getmodule(frm[1][0]).__name__.split(".")[-1]
    if vulns:
        vuln_units.extend(
            Unit(where=f"{database}://{host}:{port};{id_}", specific=[vuln])
            for id_, vuln in vulns
        )
    if safes:
        safe_units.extend(
            Unit(where=f"{database}://{host}:{port};{id_}", specific=[safe])
            for id_, safe in safes
        )

    if vulns:
        return OPEN, msg_open, vuln_units, safe_units
    return CLOSED, msg_closed, vuln_units, safe_units
