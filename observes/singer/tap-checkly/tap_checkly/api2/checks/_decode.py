from ._core import (
    Check,
    CheckObj,
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
from tap_checkly.api2.id_objs import (
    CheckGroupId,
    CheckId,
    IndexedObj,
)


def from_raw(raw: JsonObj) -> Check:
    return Check(
        Unfolder(raw["name"]).to_primitive(str).unwrap(),
        Unfolder(raw["activated"]).to_primitive(bool).unwrap(),
        Unfolder(raw["muted"]).to_primitive(bool).unwrap(),
        Unfolder(raw["doubleCheck"]).to_primitive(bool).unwrap(),
        Unfolder(raw["sslCheck"]).to_primitive(bool).unwrap(),
        Unfolder(raw["shouldFail"]).to_primitive(bool).unwrap(),
        Unfolder(raw["locations"]).to_list_of(str).unwrap(),
        Unfolder(raw["useGlobalAlertSettings"]).to_primitive(bool).unwrap(),
        Unfolder(raw["groupId"]).to_primitive(str).map(CheckGroupId).unwrap(),
        Unfolder(raw["groupOrder"]).to_primitive(int).unwrap(),
        Unfolder(raw["runtimeId"]).to_primitive(str).unwrap(),
        Unfolder(raw["checkType"]).to_primitive(str).unwrap(),
        Unfolder(raw["frequency"]).to_primitive(int).unwrap(),
        Unfolder(raw["frequencyOffset"]).to_primitive(int).unwrap(),
        Unfolder(raw["degradedResponseTime"]).to_primitive(int).unwrap(),
        Unfolder(raw["maxResponseTime"]).to_primitive(int).unwrap(),
        Unfolder(raw["created_at"]).to_primitive(str).map(isoparse).unwrap(),
        Unfolder(raw["updated_at"]).to_primitive(str).map(isoparse).unwrap(),
    )


def id_from_raw(raw: JsonObj) -> CheckId:
    return Unfolder(raw["id"]).to_primitive(str).map(CheckId).unwrap()


def from_raw_obj(raw: JsonObj) -> CheckObj:
    _id = id_from_raw(raw)
    return IndexedObj(_id, from_raw(raw))
