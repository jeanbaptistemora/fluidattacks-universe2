# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# this is necessary because of pylint error thrown only in backend-async
# module about UPPER_CASE naming style with every variable declared here
# pylint: disable-all

from typing import (
    Any,
    Dict,
    NamedTuple,
)

# Payloads
DynamoDelete = NamedTuple("DynamoDelete", [("Key", Dict[str, Any])])
