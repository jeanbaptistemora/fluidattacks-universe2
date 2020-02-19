# -*- coding: utf-8 -*-

"""Fluid Asserts AWS cloud package."""

# standard imports
import inspect
from typing import List

# 3rd party imports
import boto3

# local imports
from fluidasserts import Unit, OPEN, CLOSED


def _get_identity_info(key_id: str,
                       secret: str,
                       session_token: str = None):
    """Get information about an identity."""
    client = boto3.client(
        'sts',
        aws_access_key_id=key_id,
        aws_secret_access_key=secret,
        aws_session_token=session_token)
    return client.get_caller_identity()


def _get_result_as_tuple(*,
                         service: str, objects: str,
                         msg_open: str, msg_closed: str,
                         vulns: List[str], safes: List[str]) -> tuple:
    """Return the tuple version of the Result object."""
    vuln_units: List[Unit] = []
    safe_units: List[Unit] = []

    # Example:
    # - where: AWS/EC2/vpc-00fc6258883d60e5b
    #   specific: must be used or deleted
    frm = inspect.stack()
    arg = frm[1][0].f_locals
    identity = _get_identity_info(
        arg['key_id'], arg['secret'], arg['session_token'])
    account = identity["Account"]
    if vulns:
        vuln_units.extend(Unit(where=f'AWS/{service}/account:{account}/{id_}',
                               specific=[vuln]) for id_, vuln in vulns)
    if safes:
        safe_units.extend(Unit(where=f'AWS/{service}/account:{account}/{id_}',
                               specific=[safe]) for id_, safe in safes)

    if vulns:
        return OPEN, msg_open, vuln_units, safe_units
    if safes:
        return CLOSED, msg_closed, vuln_units, safe_units
    return CLOSED, f'No {objects} found to check', vuln_units, safe_units
