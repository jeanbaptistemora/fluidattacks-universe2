# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Fluid Asserts AWS cloud package."""


import boto3
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
)
from contextlib import (
    suppress,
)
from fluidasserts import (
    CLOSED,
    OPEN,
    Unit,
)
import inspect
from typing import (
    List,
)


def _get_identity_info(key_id: str, secret: str, session_token: str = None):
    """Get information about an identity."""
    client = boto3.client(
        "sts",
        aws_access_key_id=key_id,
        aws_secret_access_key=secret,
        aws_session_token=session_token,
    )
    return client.get_caller_identity()


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

    # Example:
    # - where: AWS/EC2/vpc-00fc6258883d60e5b
    #   specific: must be used or deleted
    frm = inspect.stack()
    arg = frm[1][0].f_locals
    account = "unrecognized"
    with suppress(BotoCoreError, ClientError):
        identity = _get_identity_info(
            arg["key_id"], arg["secret"], arg["session_token"]
        )
        account = identity["Account"]

    if vulns:
        vuln_units.extend(
            Unit(
                where=f"AWS/{service}/account:{account}/{id_}", specific=[vuln]
            )
            for id_, vuln in vulns
        )
    if safes:
        safe_units.extend(
            Unit(
                where=f"AWS/{service}/account:{account}/{id_}", specific=[safe]
            )
            for id_, safe in safes
        )

    if vulns:
        return OPEN, msg_open, vuln_units, safe_units
    if safes:
        return CLOSED, msg_closed, vuln_units, safe_units
    return CLOSED, f"No {objects} found to check", vuln_units, safe_units
