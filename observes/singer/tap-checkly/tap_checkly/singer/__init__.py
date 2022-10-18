# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _alert_channels,
    _checks,
    _groups,
)
from ._checks import (
    status,
)
from ._core import (
    SingerStreams,
)
from ._encoder import (
    ObjEncoder,
)
from dataclasses import (
    dataclass,
)
from tap_checkly.objs import (
    AlertChannelObj,
    CheckGroupObj,
    CheckObj,
    CheckStatusObj,
)


@dataclass(frozen=True)
class ObjsEncoders:
    checks: ObjEncoder[CheckObj]
    alerts: ObjEncoder[AlertChannelObj]
    groups: ObjEncoder[CheckGroupObj]
    status: ObjEncoder[CheckStatusObj]


encoders = ObjsEncoders(
    _checks.encoder, _alert_channels.encoder, _groups.encoder, status.encoder
)


__all__ = [
    "ObjEncoder",
    "SingerStreams",
]
