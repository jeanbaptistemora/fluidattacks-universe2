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
    ReportObj,
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
_date_time_type = JSchemaFactory.datetime_schema()
_bool_type = JSchemaFactory.from_prim_type(bool)
_float_type = JSchemaFactory.from_prim_type(float)


def _core_encoder_fx() -> SingerEncoder[ReportObj]:
    _mapper: Dict[str, EncodeItem[ReportObj]] = {
        "from_date": EncodeItem.new(
            lambda x: x.id_obj.from_date.date_time.isoformat(),
            Property(_date_time_type, True, False),
            ReportObj,
        ),
        "to_date": EncodeItem.new(
            lambda x: x.id_obj.to_date.date_time.isoformat(),
            Property(_date_time_type, True, False),
            ReportObj,
        ),
        "check_id": EncodeItem.new(
            lambda x: x.obj.check_id.id_str,
            Property(_str_type, False, False),
            ReportObj,
        ),
        "check_type": EncodeItem.new(
            lambda x: x.obj.check_type,
            Property(_str_type, False, False),
            ReportObj,
        ),
        "deactivated": EncodeItem.new(
            lambda x: x.obj.deactivated,
            Property(_bool_type, False, False),
            ReportObj,
        ),
        "name": EncodeItem.new(
            lambda x: x.obj.name,
            Property(_str_type, False, False),
            ReportObj,
        ),
        "avg": EncodeItem.new(
            lambda x: x.obj.avg,
            Property(_float_type, False, False),
            ReportObj,
        ),
        "p95": EncodeItem.new(
            lambda x: x.obj.p95,
            Property(_float_type, False, False),
            ReportObj,
        ),
        "p99": EncodeItem.new(
            lambda x: x.obj.p99,
            Property(_float_type, False, False),
            ReportObj,
        ),
        "success_ratio": EncodeItem.new(
            lambda x: x.obj.success_ratio,
            Property(_float_type, False, False),
            ReportObj,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.check_reports.value, freeze(_mapper)
    )


_core_encoder = _core_encoder_fx()

obj_encoder: ObjEncoder[ReportObj] = ObjEncoder.new(
    from_flist((_core_encoder.schema,)),
    lambda x: from_flist((_core_encoder.record(x),)),
    ReportObj,
)
