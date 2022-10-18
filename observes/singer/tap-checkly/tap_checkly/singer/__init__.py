# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _alert_channels,
    _checks,
    _groups,
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
)
from typing import (
    NamedTuple,
)


@dataclass(frozen=True)
class ObjsEncoders:
    checks: ObjEncoder[CheckObj]
    alerts: ObjEncoder[AlertChannelObj]
    groups: ObjEncoder[CheckGroupObj]


encoders = ObjsEncoders(
    _checks.encoder, _alert_channels.encoder, _groups.encoder
)


__all__ = [
    "SingerStreams",
]
