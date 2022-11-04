# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
from . import (
    _api,
    _browser,
    _core,
)
from fa_purity import (
    FrozenList,
    PureIter,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_singer_io.singer import (
    SingerRecord,
)
from tap_checkly.objs import (
    CheckResultObj,
    IndexedObj,
)
from tap_checkly.singer._encoder import (
    ObjEncoder,
)


def _to_records(item: CheckResultObj) -> PureIter[SingerRecord]:
    empty: FrozenList[SingerRecord] = tuple([])
    records = (
        item.obj.api_result.map(
            lambda r: _api.encoder.record(IndexedObj(item.id_obj, r))
        )
        .map(lambda i: tuple([i]))
        .value_or(empty)
    ) + (_core.encoder.record(item),)
    return from_flist(records)


_schemas = (
    _core.encoder.schema,
    _api.encoder.schema,
) + tuple(_browser.encoder.schemas)
encoder: ObjEncoder[CheckResultObj] = ObjEncoder.new(
    from_flist(_schemas),
    _to_records,
)
