# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._core import (
    AlertChannel,
    AlertChannelId,
    AlertChannelObj,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    JsonObj,
    Maybe,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from tap_checkly.objs import (
    IndexedObj,
)


def from_raw(raw: JsonObj) -> AlertChannel:
    return AlertChannel(
        Unfolder(raw["type"]).to_primitive(str).unwrap(),
        Unfolder(raw["sendRecovery"]).to_primitive(bool).unwrap(),
        Unfolder(raw["sendFailure"]).to_primitive(bool).unwrap(),
        Unfolder(raw["sendDegraded"]).to_primitive(bool).unwrap(),
        Unfolder(raw["sslExpiry"]).to_primitive(bool).unwrap(),
        Unfolder(raw["sslExpiryThreshold"]).to_primitive(int).unwrap(),
        Unfolder(raw["created_at"]).to_primitive(str).map(isoparse).unwrap(),
        Unfolder(raw["updated_at"])
        .to_optional(lambda x: x.to_primitive(str))
        .map(lambda x: Maybe.from_optional(x).map(isoparse))
        .unwrap(),
    )


def from_raw_obj(raw: JsonObj) -> AlertChannelObj:
    _id = Unfolder(raw["id"]).to_primitive(int).map(AlertChannelId).unwrap()
    return IndexedObj(_id, from_raw(raw))
