# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity.frozen import (
    freeze,
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
    CheckResultObj,
)
from tap_checkly.singer._core import (
    SingerStreams,
)
from typing import (
    Dict,
)

_str_type = JSchemaFactory.from_prim_type(str)
_int_type = JSchemaFactory.from_prim_type(int)
_bool_type = JSchemaFactory.from_prim_type(bool)
_date_type = JSchemaFactory.datetime_schema()


def _encoder() -> SingerEncoder[CheckResultObj]:
    _mapper: Dict[str, EncodeItem[CheckResultObj]] = {
        "check_id": EncodeItem.new(
            lambda x: x.id_obj[0].id_str,
            Property(_str_type, True, False),
            CheckResultObj,
        ),
        "result_id": EncodeItem.new(
            lambda x: x.id_obj[1].id_str,
            Property(_str_type, True, False),
            CheckResultObj,
        ),
        "attempts": EncodeItem.new(
            lambda x: x.obj.attempts,
            Property(_int_type, False, False),
            CheckResultObj,
        ),
        "run_id": EncodeItem.new(
            lambda x: x.obj.run_id.id_num,
            Property(_int_type, False, False),
            CheckResultObj,
        ),
        "created_at": EncodeItem.new(
            lambda x: x.obj.created_at.isoformat(),
            Property(_date_type, False, False),
            CheckResultObj,
        ),
        "has_errors": EncodeItem.new(
            lambda x: x.obj.has_errors,
            Property(_bool_type, False, False),
            CheckResultObj,
        ),
        "has_failures": EncodeItem.new(
            lambda x: x.obj.has_failures,
            Property(_bool_type, False, False),
            CheckResultObj,
        ),
        "is_degraded": EncodeItem.new(
            lambda x: x.obj.is_degraded,
            Property(_bool_type, False, False),
            CheckResultObj,
        ),
        "over_max_response_time": EncodeItem.new(
            lambda x: x.obj.over_max_response_time,
            Property(_bool_type, False, False),
            CheckResultObj,
        ),
        "response_time": EncodeItem.new(
            lambda x: x.obj.response_time,
            Property(_int_type, False, False),
            CheckResultObj,
        ),
        "run_location": EncodeItem.new(
            lambda x: x.obj.run_location,
            Property(_str_type, False, False),
            CheckResultObj,
        ),
        "started_at": EncodeItem.new(
            lambda x: x.obj.started_at.isoformat(),
            Property(_date_type, False, False),
            CheckResultObj,
        ),
        "stopped_at": EncodeItem.new(
            lambda x: x.obj.stopped_at.isoformat(),
            Property(_date_type, False, False),
            CheckResultObj,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.check_results.value, freeze(_mapper)
    )


encoder = _encoder()
