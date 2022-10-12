# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    FrozenDict,
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
from fa_singer_io.singer.schema.core import (
    Property,
    SingerSchema,
)
from tap_checkly.singer.core import (
    SingerStreams,
)

_str_type = JSchemaFactory.from_prim_type(str)
_int_type = JSchemaFactory.from_prim_type(int)
_bool_type = JSchemaFactory.from_prim_type(bool)
_date_type = JSchemaFactory.datetime_schema()


def _core_schema() -> SingerSchema:
    _props: FrozenDict[str, Property] = freeze(
        {
            "id": Property(_str_type, True, False),
            "name": Property(_str_type, False, False),
            "created_at": Property(_date_type, False, False),
            "updated_at": Property(_date_type, False, False),
            "activated": Property(_bool_type, False, False),
            "muted": Property(_bool_type, False, False),
            "double_check": Property(_bool_type, False, False),
            "ssl_check": Property(_bool_type, False, False),
            "should_fail": Property(_bool_type, False, False),
            "use_global_alert_settings": Property(_bool_type, False, False),
            "group_id": Property(_int_type, False, False),
            "group_order": Property(_int_type, False, False),
            "runtime_ver": Property(_str_type, False, False),
            "check_type": Property(_str_type, False, False),
            "frequency": Property(_int_type, False, False),
            "frequency_offset": Property(_int_type, False, False),
            "degraded_response_time": Property(_int_type, False, False),
            "max_response_time": Property(_int_type, False, False),
        }
    )
    return SingerSchema.obj_schema(SingerStreams.checks.value, _props)


def _locations_schema() -> SingerSchema:
    _props: FrozenDict[str, Property] = freeze(
        {
            "id": Property(_str_type, True, False),
            "index": Property(_int_type, True, False),
            "location": Property(_str_type, False, False),
        }
    )
    return SingerSchema.obj_schema(SingerStreams.checks.value, _props)


def json_schemas() -> PureIter[SingerSchema]:
    return from_flist((_core_schema(), _locations_schema()))
