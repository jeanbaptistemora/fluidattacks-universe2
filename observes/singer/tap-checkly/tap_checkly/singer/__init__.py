# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _alert_channels,
    _checks,
)
from ._encoder import (
    ObjEncoder,
)
from dataclasses import (
    dataclass,
)
from tap_checkly.api2.alert_channels import (
    AlertChannelObj,
)
from tap_checkly.api2.checks import (
    CheckObj,
)


@dataclass(frozen=True)
class ObjsEncoders:
    checks: ObjEncoder[CheckObj]
    alerts: ObjEncoder[AlertChannelObj]


def encoders() -> ObjsEncoders:
    return ObjsEncoders(_checks.encoder, _alert_channels.encoder)
