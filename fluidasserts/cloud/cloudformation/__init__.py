# -*- coding: utf-8 -*-

"""Fluid Asserts AWS cloud package."""

# standard imports
from typing import List, NamedTuple

# local imports
from fluidasserts import Unit, OPEN, CLOSED

# Containers
Vulnerability = NamedTuple('Vulnerability', [
    ('path', str),
    ('service', str),
    ('identifier', str),
    ('reason', str),
])


def _get_result_as_tuple(*,
                         vulnerabilities: List[Vulnerability],
                         msg_open: str, msg_closed: str) -> tuple:
    """Return the tuple version of the Result object."""
    # Example:
    # - where: {path}
    #   specific: {service}/{id} {reason}

    vuln_units: List[Unit] = [
        Unit(where=x.path,
             specific=[f'{x.service}/{x.identifier} {x.reason}'])
        for x in vulnerabilities]

    if vuln_units:
        return OPEN, msg_open, vuln_units
    return CLOSED, msg_closed, vuln_units
