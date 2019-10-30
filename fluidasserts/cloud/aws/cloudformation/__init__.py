"""Fluid Asserts AWS cloud package."""

# standard imports
from typing import List, NamedTuple

# local imports
from fluidasserts import Unit, OPEN, CLOSED

# Containers
Vulnerability = NamedTuple('Vulnerability', [
    ('path', str),
    ('entity', str),
    ('identifier', str),
    ('reason', str),
])


def _get_result_as_tuple(*,
                         vulnerabilities: List[Vulnerability],
                         msg_open: str, msg_closed: str) -> tuple:
    """Return the tuple version of the Result object."""
    # Example:
    # - where: {path}
    #   specific: {entity}/{id} {reason}

    vuln_units: List[Unit] = [
        Unit(where=x.path,
             specific=[f'{x.entity}/{x.identifier} {x.reason}'])
        for x in vulnerabilities]

    if vuln_units:
        return OPEN, msg_open, vuln_units
    return CLOSED, msg_closed, vuln_units


class CloudFormationError(Exception):
    """Base class for all errors in this module."""


class CloudFormationInvalidTypeError(CloudFormationError):
    """The Value is not of recognized type."""


class CloudFormationInvalidTemplateError(CloudFormationError):
    """The template is not JSON or YAML compliant."""
