# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    PureIter,
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
from fa_singer_io.singer import (
    SingerRecord,
)
from fa_singer_io.singer.encoder import (
    EncodeItem,
    SingerEncoder,
)
from fa_singer_io.singer.schema.core import (
    Property,
)
from tap_checkly.objs import (
    CheckStatusObj,
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


def _core_encoder_fx() -> SingerEncoder[CheckStatusObj]:
    _mapper: Dict[str, EncodeItem[CheckStatusObj]] = {
        "check_id": EncodeItem.new(
            lambda x: x.id_obj.id_str,
            Property(_str_type, True, False),
            CheckStatusObj,
        ),
        "name": EncodeItem.new(
            lambda x: x.obj.name,
            Property(_str_type, False, False),
            CheckStatusObj,
        ),
        "created_at": EncodeItem.new(
            lambda x: x.obj.created_at.isoformat(),
            Property(_date_type, False, False),
            CheckStatusObj,
        ),
        "has_errors": EncodeItem.new(
            lambda x: x.obj.has_errors,
            Property(_bool_type, False, False),
            CheckStatusObj,
        ),
        "has_failures": EncodeItem.new(
            lambda x: x.obj.has_failures,
            Property(_bool_type, False, False),
            CheckStatusObj,
        ),
        "is_degraded": EncodeItem.new(
            lambda x: x.obj.is_degraded,
            Property(_bool_type, False, False),
            CheckStatusObj,
        ),
        "last_check_run_id": EncodeItem.new(
            lambda x: x.obj.last_check_run_id,
            Property(_str_type, False, False),
            CheckStatusObj,
        ),
        "last_run_location": EncodeItem.new(
            lambda x: x.obj.last_run_location,
            Property(_str_type, False, False),
            CheckStatusObj,
        ),
        "longest_run": EncodeItem.new(
            lambda x: x.obj.longest_run,
            Property(_int_type, False, False),
            CheckStatusObj,
        ),
        "shortest_run": EncodeItem.new(
            lambda x: x.obj.shortest_run,
            Property(_int_type, False, False),
            CheckStatusObj,
        ),
        "ssl_days_remaining": EncodeItem.new(
            lambda x: x.obj.ssl_days_remaining,
            Property(_int_type, False, False),
            CheckStatusObj,
        ),
        "updated_at": EncodeItem.new(
            lambda x: x.obj.updated_at.map(lambda d: d.isoformat()).value_or(
                None
            ),
            Property(JSchemaFactory.opt_datetime_schema(), False, False),
            CheckStatusObj,
        ),
    }
    return SingerEncoder.new(SingerStreams.checks.value, freeze(_mapper))


_status_encoder = _core_encoder_fx()


def _to_records(item: CheckStatusObj) -> PureIter[SingerRecord]:
    _records = (_status_encoder.record(item),)
    return from_flist(_records)


encoder: ObjEncoder[CheckStatusObj] = ObjEncoder.new(
    from_flist((_status_encoder.schema,)),
    _to_records,
)
