from . import (
    _alert_channels,
    _checks,
    _groups,
    _report,
)
from ._checks import (
    results,
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
from fa_purity import (
    FrozenList,
)
from tap_checkly.objs import (
    AlertChannelObj,
    CheckGroupObj,
    CheckObj,
    CheckReport,
    CheckResultObj,
    CheckStatusObj,
)


@dataclass(frozen=True)
class ObjsEncoders:
    checks: ObjEncoder[CheckObj]
    alerts: ObjEncoder[AlertChannelObj]
    groups: ObjEncoder[CheckGroupObj]
    status: ObjEncoder[CheckStatusObj]
    report: ObjEncoder[CheckReport]
    bulk_reports: ObjEncoder[FrozenList[CheckReport]]
    results: ObjEncoder[CheckResultObj]


encoders = ObjsEncoders(
    _checks.encoder,
    _alert_channels.encoder,
    _groups.encoder,
    status.encoder,
    _report.encoder,
    _report.bulk_encoder,
    results.encoder,
)


__all__ = [
    "ObjEncoder",
    "SingerStreams",
]
