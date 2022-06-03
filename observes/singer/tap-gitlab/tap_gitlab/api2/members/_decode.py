from ._core import (
    Member,
    User,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    JsonObj,
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
        Unfolder(raw["email"]).to_primitive(str).unwrap(),
        Unfolder(raw["name"]).to_primitive(str).unwrap(),
        Unfolder(raw["state"]).to_primitive(str).unwrap(),
        Unfolder(raw["created_at"]).to_primitive(str).map(isoparse).unwrap(),
        Unfolder(raw["is_admin"]).to_primitive(bool).unwrap(),
    )
    return Member(
        (_id, user),
        Unfolder(raw["membership_state"]).to_primitive(str).unwrap(),
    )
