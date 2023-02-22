from collections import (
    OrderedDict,
)
import dataclasses
from datetime import (
    date,
    datetime,
)
from dateutil.parser import (
    parse as date_parser,
)
from decimal import (
    Decimal,
)
from enum import (
    Enum,
)
import json
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)

# Constants
TVar = TypeVar("TVar")

# Factory signature, args, kwargs
Serialized = Tuple[Tuple[str, str], Tuple[Any, ...], Dict[str, Any]]


class LoadError(Exception):
    pass


def _bytes_dump(instance: bytes) -> Serialized:
    return serialize(instance, instance.hex())


def _bytes_load(data: str) -> bytes:
    return bytes.fromhex(data)


def _dataclass_dump(instance: Any) -> Serialized:
    return serialize(instance, *map(dump_raw, dataclasses.astuple(instance)))


def _dataclass_load(factory: Callable[..., TVar]) -> Callable[..., TVar]:
    return lambda *args: factory(*map(_deserialize, args))


def _datetime_dump(time: datetime) -> Serialized:
    return serialize(time, time.isoformat())


def _datetime_load(time: str) -> datetime:
    return date_parser(time)


def _decimal_dump(data: Decimal) -> Serialized:
    return serialize(data, data.to_eng_string())


def _decimal_load(data: str) -> Decimal:
    return Decimal(data)


def _dict_dump(instance: Dict[str, Any]) -> Serialized:
    return serialize(
        instance,
        *((dump_raw(key), dump_raw(val)) for key, val in instance.items()),
    )


def _dict_load(*args: Tuple[Serialized, Serialized]) -> Dict[Any, Any]:
    return dict((_deserialize(key), _deserialize(val)) for key, val in args)


def _enum_dump(instance: Enum) -> Serialized:
    return serialize(instance, dump_raw(instance.value))


def _enum_load(factory: Callable[..., TVar]) -> Callable[..., TVar]:
    return lambda value: factory(_deserialize(value))


def list_load(*args: Serialized) -> List[Any]:
    return list(_tuple_load(*args))


def _namedtuple_dump(instance: Tuple[Any, ...]) -> Serialized:
    return serialize(instance, *map(dump_raw, instance))


def _namedtuple_load(factory: Callable[..., TVar]) -> Callable[..., TVar]:
    return lambda *args: factory(*map(_deserialize, args))


def _none_dump(instance: None) -> Serialized:
    return serialize(instance)


def _none_load() -> None:
    return None


def _ordereddict_load(*args: Tuple[Serialized, Serialized]) -> Dict[Any, Any]:
    return OrderedDict(_dict_load(*args))


def tuple_dump(instance: List[Any]) -> Serialized:
    return serialize(instance, *map(dump_raw, instance))


def _tuple_load(*args: Serialized) -> Tuple[Any, ...]:
    return tuple(map(_deserialize, args))


def _idem_dump(obj: Any) -> Serialized:
    return serialize(obj, obj)


# This is what guarantees security, only this types are whitelisted
ALLOWED_FACTORIES: Dict[type, Dict[str, Any]] = {}
SIGNATURE_TO_FACTORY: Dict[Any, type] = {}


def register(
    factory: Type[TVar],
    dumper: Callable[[TVar], Serialized],
    loader: Callable[..., TVar],
) -> None:
    signature = (factory.__module__, factory.__name__)
    ALLOWED_FACTORIES[factory] = dict(
        dumper=dumper,
        loader=loader,
        signature=signature,
    )
    SIGNATURE_TO_FACTORY[signature] = factory


def register_dataclass(type_: Any) -> None:
    register(type_, _dataclass_dump, _dataclass_load(type_))


def register_enum(type_: Any) -> None:
    register(type_, _enum_dump, _enum_load(type_))


def register_namedtuple(type_: Any) -> None:
    register(type_, _namedtuple_dump, _namedtuple_load(type_))


def _side_effects() -> None:
    for factory, dumper, loader in (
        (bool, _idem_dump, bool),
        (bytes, _bytes_dump, _bytes_load),
        (dict, _dict_dump, _dict_load),
        (date, _datetime_dump, _datetime_load),
        (datetime, _datetime_dump, _datetime_load),
        (Decimal, _decimal_dump, _decimal_load),
        (float, _idem_dump, float),
        (int, _idem_dump, int),
        (list, tuple_dump, list_load),
        (OrderedDict, _dict_dump, _ordereddict_load),
        (str, _idem_dump, str),
        (tuple, tuple_dump, _tuple_load),
        (type(None), _none_dump, _none_load),
    ):
        register(factory, dumper, loader)


def serialize(
    instance: Any,
    *args: Any,
    **kwargs: Any,
) -> Serialized:
    signature = ALLOWED_FACTORIES[type(instance)]["signature"]

    return (signature, args, kwargs)


def _deserialize(data: Serialized) -> Any:
    signature, args, kwargs = tuple(data[0]), data[1], data[2]
    factory: type = SIGNATURE_TO_FACTORY[signature]
    loader: Callable[..., Any] = ALLOWED_FACTORIES[factory]["loader"]

    return loader(*args, **kwargs)


def dump_raw(instance: Any) -> Serialized:
    factory = type(instance)
    dumper: Callable[..., Serialized] = ALLOWED_FACTORIES[factory]["dumper"]

    return dumper(instance)


def dump(instance: Any, ttl: Optional[int] = None) -> bytes:
    dumped: Serialized = dump_raw(instance)
    message = {
        "expires_at": (
            None if ttl is None else datetime.now().timestamp() + ttl
        ),
        "instance": dumped,
    }

    serialized: str = json.dumps(message, separators=(",", ":"))

    return serialized.encode("utf-8")


def load(stream: bytes) -> Any:
    try:
        deserialized: Any = json.loads(stream)

        expires_at: Optional[int] = deserialized["expires_at"]
        if expires_at and datetime.now().timestamp() > expires_at:
            raise LoadError("Data has expired")

        return _deserialize(deserialized["instance"])
    except (
        AttributeError,
        json.decoder.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        raise LoadError(exc)


# Side effects
_side_effects()
