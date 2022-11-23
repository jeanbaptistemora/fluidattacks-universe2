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
    AlertChannelObj,
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
_int_type = JSchemaFactory.from_prim_type(int)
_bool_type = JSchemaFactory.from_prim_type(bool)
_date_type = JSchemaFactory.datetime_schema()


def _core_encoder_fx() -> SingerEncoder[AlertChannelObj]:
    _mapper: Dict[str, EncodeItem[AlertChannelObj]] = {
        "alert_ch_id": EncodeItem.new(
            lambda x: x.id_obj.id_int,
            Property(_int_type, True, False),
            AlertChannelObj,
        ),
        "alert_type": EncodeItem.new(
            lambda x: x.obj.alert_type,
            Property(_str_type, False, False),
            AlertChannelObj,
        ),
        "send_recovery": EncodeItem.new(
            lambda x: x.obj.send_recovery,
            Property(_bool_type, False, False),
            AlertChannelObj,
        ),
        "send_failure": EncodeItem.new(
            lambda x: x.obj.send_failure,
            Property(_bool_type, False, False),
            AlertChannelObj,
        ),
        "send_degraded": EncodeItem.new(
            lambda x: x.obj.send_degraded,
            Property(_bool_type, False, False),
            AlertChannelObj,
        ),
        "ssl_expiry": EncodeItem.new(
            lambda x: x.obj.ssl_expiry,
            Property(_bool_type, False, False),
            AlertChannelObj,
        ),
        "ssl_expiry_threshold": EncodeItem.new(
            lambda x: x.obj.ssl_expiry_threshold,
            Property(_int_type, False, False),
            AlertChannelObj,
        ),
        "created_at": EncodeItem.new(
            lambda x: x.obj.created_at.isoformat(),
            Property(_date_type, False, False),
            AlertChannelObj,
        ),
        "updated_at": EncodeItem.new(
            lambda x: x.obj.updated_at.map(lambda d: d.isoformat()).value_or(
                None
            ),
            Property(JSchemaFactory.opt_datetime_schema(), False, False),
            AlertChannelObj,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.alert_channels.value, freeze(_mapper)
    )


_core_encoder = _core_encoder_fx()


encoder: ObjEncoder[AlertChannelObj] = ObjEncoder.new(
    from_flist((_core_encoder.schema,)),
    lambda x: from_flist((_core_encoder.record(x),)),
    AlertChannelObj,
)
