from fa_purity import (
    FrozenList,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_singer_io.json_schema import (
    JSchemaFactory,
)
from fa_singer_io.singer.encoder import (
    EncodeItem,
    SingerEncoder,
)
from fa_singer_io.singer.schema.core import (
    Property,
)
from tap_checkly.objs import (
    CheckReport,
)
from tap_checkly.singer._core import (
    SingerStreams,
)
from tap_checkly.singer._encoder import (
    ObjEncoder,
)
from typing import (
    Dict,
)

_str_type = JSchemaFactory.from_prim_type(str)
_bool_type = JSchemaFactory.from_prim_type(bool)
_float_type = JSchemaFactory.from_prim_type(float)


def _core_encoder_fx() -> SingerEncoder[CheckReport]:
    _mapper: Dict[str, EncodeItem[CheckReport]] = {
        "check_id": EncodeItem.new(
            lambda x: x.check_id.id_str,
            Property(_str_type, True, False),
            CheckReport,
        ),
        "check_type": EncodeItem.new(
            lambda x: x.check_type,
            Property(_str_type, False, False),
            CheckReport,
        ),
        "deactivated": EncodeItem.new(
            lambda x: x.deactivated,
            Property(_bool_type, False, False),
            CheckReport,
        ),
        "name": EncodeItem.new(
            lambda x: x.name,
            Property(_str_type, False, False),
            CheckReport,
        ),
        "avg": EncodeItem.new(
            lambda x: x.avg,
            Property(_float_type, False, False),
            CheckReport,
        ),
        "p95": EncodeItem.new(
            lambda x: x.p95,
            Property(_float_type, False, False),
            CheckReport,
        ),
        "p99": EncodeItem.new(
            lambda x: x.p99,
            Property(_float_type, False, False),
            CheckReport,
        ),
        "success_ratio": EncodeItem.new(
            lambda x: x.success_ratio,
            Property(_float_type, False, False),
            CheckReport,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.check_reports.value, freeze(_mapper)
    )


_core_encoder = _core_encoder_fx()


encoder: ObjEncoder[CheckReport] = ObjEncoder.new(
    from_flist((_core_encoder.schema,)),
    lambda x: from_flist((_core_encoder.record(x),)),
    CheckReport,
)

bulk_encoder: ObjEncoder[FrozenList[CheckReport]] = ObjEncoder.new(
    from_flist((_core_encoder.schema,)),
    lambda x: from_flist(x).map(_core_encoder.record),
    FrozenList[CheckReport],
)
