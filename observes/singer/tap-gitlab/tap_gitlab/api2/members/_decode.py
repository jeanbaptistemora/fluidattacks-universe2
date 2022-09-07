# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._core import (
    Member,
    User,
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
from tap_gitlab.api2.ids import (
    UserId,
)


def decode_member(raw: JsonObj) -> Member:
    _id = UserId(Unfolder(raw["id"]).to_primitive(int).unwrap())
    user = User(
        Unfolder(raw["username"]).to_primitive(str).unwrap(),
        Maybe.from_optional(raw.get("email")).map(
            lambda v: Unfolder(v).to_primitive(str).unwrap()
        ),
        Unfolder(raw["name"]).to_primitive(str).unwrap(),
        Unfolder(raw["state"]).to_primitive(str).unwrap(),
        Unfolder(raw["created_at"]).to_primitive(str).map(isoparse).unwrap(),
    )
    return Member(
        (_id, user),
        Unfolder(raw["membership_state"]).to_primitive(str).unwrap(),
    )
