# -*- coding: utf-8 -*-

"""Fluid Asserts Azure cloud package."""

# standard imports
from typing import List, Callable

# 3rd party imports
from azure.common.credentials import ServicePrincipalCredentials

# local imports
from fluidasserts import Unit, OPEN, CLOSED


def _get_result_as_tuple(*, objects: str,
                         msg_open: str, msg_closed: str,
                         vulns: List[str], safes: List[str]) -> tuple:
    """Return the tuple version of the Result object."""
    vuln_units: List[Unit] = []
    safe_units: List[Unit] = []

    # Example:
    # - where: Azure/subscriptions/xxxxx/resourceGroups/same/providers/
    #   Microsoft.Network/networkInterfaces/test-01948
    #   specific: must be used or deleted

    if vulns:
        vuln_units.extend(Unit(where=f'Azure{id_}',
                               specific=[vuln]) for id_, vuln in vulns)
    if safes:
        safe_units.extend(Unit(where=f'Azure/{id_}',
                               specific=[safe]) for id_, safe in safes)

    if vulns:
        return OPEN, msg_open, vuln_units, safe_units
    if safes:
        return CLOSED, msg_closed, vuln_units, safe_units
    return CLOSED, f'No {objects} found to check', vuln_units, safe_units


def _get_credentials(client_id: str, secret: str,
                     tenant: str) -> ServicePrincipalCredentials:
    return ServicePrincipalCredentials(
        client_id=client_id, secret=secret, tenant=tenant)


def _attr_checker(object_, rules: dict):
    success = []
    for key, value in rules.items():
        if isinstance(value, Callable):
            success.append(value(getattr(object_, key, None)))
        else:
            success.append(getattr(object_, key, None) in value)
    return success
