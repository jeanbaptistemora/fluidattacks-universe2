from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
)
from fa_purity.json.factory import (
    from_prim_dict,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from tap_checkly.api2._raw import (
    RawClient,
)
from tap_checkly.api2.checks.core import (
    CheckId,
)


def _check_id_from_raw(raw: JsonObj) -> CheckId:
    _id = Unfolder(raw["id"]).to_primitive(str).unwrap()
    return CheckId(_id)


@dataclass(frozen=True)
class ChecksClient:
    _raw: RawClient
    _per_page: int

    def list_checks(self, page: int) -> Cmd[FrozenList[CheckId]]:
        return self._raw.get_list(
            "/v1/checks",
            from_prim_dict({"limit": self._per_page, "page": page}),
        ).map(lambda l: tuple(map(_check_id_from_raw, l)))
