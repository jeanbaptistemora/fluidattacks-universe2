# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
from __future__ import (
    annotations,
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
    ChannelSubscription,
    CheckGroupId,
    CheckGroupObj,
)
from typing import (
    Dict,
)

_str_type = JSchemaFactory.from_prim_type(str)
_int_type = JSchemaFactory.from_prim_type(int)
_bool_type = JSchemaFactory.from_prim_type(bool)
_date_type = JSchemaFactory.datetime_schema()


def _core_encoder_fx() -> SingerEncoder[CheckGroupObj]:
    _mapper: Dict[str, EncodeItem[CheckGroupObj]] = {
        "group_id": EncodeItem.new(
            lambda x: x.id_obj.id_str,
            Property(_int_type, True, False),
            CheckGroupObj,
        ),
        "activated": EncodeItem.new(
            lambda x: x.obj.activated,
            Property(_bool_type, False, False),
            CheckGroupObj,
        ),
        "concurrency": EncodeItem.new(
            lambda x: x.obj.concurrency,
            Property(_int_type, False, False),
            CheckGroupObj,
        ),
        "name": EncodeItem.new(
            lambda x: x.obj.name,
            Property(_str_type, False, False),
            CheckGroupObj,
        ),
        "created_at": EncodeItem.new(
            lambda x: x.obj.created_at.isoformat(),
            Property(_date_type, False, False),
            CheckGroupObj,
        ),
        "updated_at": EncodeItem.new(
            lambda x: x.obj.updated_at.map(lambda d: d.isoformat()).value_or(
                None
            ),
            Property(JSchemaFactory.opt_datetime_schema(), False, False),
            CheckGroupObj,
        ),
        # alert_channels
        "double_check": EncodeItem.new(
            lambda x: x.obj.double_check,
            Property(_bool_type, False, False),
            CheckGroupObj,
        ),
        # locations
        "muted": EncodeItem.new(
            lambda x: x.obj.muted,
            Property(_bool_type, False, False),
            CheckGroupObj,
        ),
        "runtime_id": EncodeItem.new(
            lambda x: x.obj.runtime_id,
            Property(_str_type, False, False),
            CheckGroupObj,
        ),
        "use_global_alert_settings": EncodeItem.new(
            lambda x: x.obj.use_global_alert_settings,
            Property(_bool_type, False, False),
            CheckGroupObj,
        ),
    }
    return SingerEncoder.new(SingerStreams.check_groups.value, freeze(_mapper))


@dataclass(frozen=True)
class GroupAlert:
    group: CheckGroupId
    sub: ChannelSubscription

    @staticmethod
    def from_group_obj(item: CheckGroupObj) -> PureIter[GroupAlert]:
        return from_flist(item.obj.alert_channels).map(
            lambda s: GroupAlert(item.id_obj, s),
        )


def _group_alert_encoder_fx() -> SingerEncoder[GroupAlert]:
    _mapper: Dict[str, EncodeItem[GroupAlert]] = {
        "group_id": EncodeItem.new(
            lambda x: x.group.id_str,
            Property(_int_type, True, False),
            GroupAlert,
        ),
        "activated": EncodeItem.new(
            lambda x: x.sub.activated,
            Property(_bool_type, False, False),
            GroupAlert,
        ),
        "channel_id": EncodeItem.new(
            lambda x: x.sub.channel.id_int,
            Property(_int_type, False, False),
            GroupAlert,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.check_groups_alerts.value, freeze(_mapper)
    )


@dataclass(frozen=True)
class LocationItem:
    group_id: CheckGroupId
    index: int
    location: str

    @staticmethod
    def from_group_obj(item: CheckGroupObj) -> PureIter[LocationItem]:
        return (
            from_flist(item.obj.locations)
            .enumerate(0)
            .map(
                lambda t: LocationItem(
                    item.id_obj,
                    t[0],
                    t[1],
                ),
            )
        )


def _locations_encoder_fx() -> SingerEncoder[LocationItem]:
    _mapper: Dict[str, EncodeItem[LocationItem]] = {
        "group_id": EncodeItem.new(
            lambda x: x.group_id.id_str,
            Property(_str_type, True, False),
            LocationItem,
        ),
        "index": EncodeItem.new(
            lambda x: x.index,
            Property(_int_type, True, False),
            LocationItem,
        ),
        "location": EncodeItem.new(
            lambda x: x.location,
            Property(_str_type, False, False),
            LocationItem,
        ),
    }
    return SingerEncoder.new(
        SingerStreams.check_groups_locations.value, freeze(_mapper)
    )


_core_encoder = _core_encoder_fx()
_locations_encoder = _locations_encoder_fx()
_group_alert_encoder = _group_alert_encoder_fx()


def _to_records(item: CheckGroupObj) -> PureIter[SingerRecord]:
    _records = (
        LocationItem.from_group_obj(item)
        .map(lambda l: _locations_encoder.record(l))
        .to_list()
        + GroupAlert.from_group_obj(item)
        .map(lambda l: _group_alert_encoder.record(l))
        .to_list()
        + (_core_encoder.record(item),)
    )
    return from_flist(_records)


encoder: ObjEncoder[CheckGroupObj] = ObjEncoder.new(
    from_flist(
        (
            _core_encoder.schema,
            _group_alert_encoder.schema,
            _locations_encoder.schema,
        )
    ),
    _to_records,
)
