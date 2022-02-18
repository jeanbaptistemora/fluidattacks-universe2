# pylint: skip-file

from postgres_client.column import (
    RedshiftDataType,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    Any,
    Dict,
    Tuple,
    Union,
)


class InvalidType(Exception):
    pass


class UnsupportedMultipleTypes(Exception):
    pass


class NullOrEmptyType(Exception):
    pass


raw_type_map: Dict[str, RedshiftDataType] = {
    "boolean": RedshiftDataType.BOOLEAN,
    "integer": RedshiftDataType.BIGINT,
    "number": RedshiftDataType.DOUBLE_PRECISION,
    "string": RedshiftDataType.VARCHAR,
}


def _rm_null(obj_type: Union[str, Tuple[str, ...]]) -> str:
    if isinstance(obj_type, str):
        return obj_type
    match = tuple(filter(lambda x: x != "null", obj_type))
    if match:
        if len(match) < 2:
            return match[0]
        raise UnsupportedMultipleTypes()
    raise NullOrEmptyType()


def _validate_type(obj_type: Any) -> Union[str, Tuple[str, ...]]:
    if isinstance(obj_type, str):
        return obj_type
    if isinstance(obj_type, list) and all(
        map(lambda x: isinstance(x, str), obj_type)
    ):
        return tuple(obj_type)
    raise InvalidType(f"{obj_type} expected str or tuple[str,...]")


def _validate_format(obj_type: Any) -> str:
    if isinstance(obj_type, str):
        return obj_type
    raise InvalidType(f"{obj_type} expected str")


def _to_rs_data_type(
    obj_type: str, obj_format: Maybe[str]
) -> RedshiftDataType:
    if obj_type == "string":
        is_timestamp = obj_format.map(lambda x: x == "date-time").or_else_call(
            lambda: False
        )
        if is_timestamp:
            return RedshiftDataType.TIMESTAMP
    return raw_type_map[obj_type]


def from_json(obj: Dict[str, Any]) -> RedshiftDataType:
    _type = _rm_null(_validate_type(obj["type"]))
    _format = Maybe.from_optional(obj.get("format")).map(_validate_format)
    return _to_rs_data_type(_type, _format)
