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
            success.append(value(getattr(object_, key, '')))
        else:
            success.append(getattr(object_, key, '') in value)
    return success


def _port_in_range(port, range_):
    success = False
    port = str(port)
    if isinstance(range_, list):
        success = any([_port_in_range(port, range__) for range__ in range_])
    elif '*' in range_:
        success = True
    elif port in range_:
        success = True
    elif '-' in range_:
        ran = range_.split('-')
        success = int(port) in range(int(ran[0]), int(ran[1]))
    return success


def _flatten(elements, aux_list=None):
    aux_list = aux_list if aux_list is not None else []
    for i in elements:
        if isinstance(i, list):
            _flatten(i, aux_list)
        else:
            aux_list.append(i)
    return aux_list
