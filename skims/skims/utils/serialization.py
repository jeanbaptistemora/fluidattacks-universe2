# Standard libraries
from collections import (
    OrderedDict,
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
    TypeVar,
)
# Third party libraries
from aioextensions import (
    in_process,
)

# Local libraries
from utils.logs import (
    log_exception,
)
from utils.model import (
    FindingEnum,
    FindingMetadata,
    FindingTypeEnum,
    IntegratesVulnerabilityMetadata,
    NVDVulnerability,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityApprovalStatusEnum,
    VulnerabilityKindEnum,
    VulnerabilitySourceEnum,
    VulnerabilityStateEnum,
)
from utils.time import (
    get_utc_timestamp,
)

# Constants
TVar = TypeVar('TVar')

# Factory signature, args, kwargs
Serialized = Tuple[Tuple[str, str], Tuple[Any, ...], Dict[str, Any]]


class LoadError(Exception):
    pass


def _dump_bytes(instance: bytes) -> Serialized:
    return _serialize(instance, instance.hex())


def _load_bytes(data: str) -> bytes:
    return bytes.fromhex(data)


def _dump_dict(instance: Dict[str, Any]) -> Serialized:
    return _serialize(
        instance, *((_dump(key), _dump(val)) for key, val in instance.items()),
    )


def _load_dict(*args: Tuple[Serialized, Serialized]) -> Dict[Any, Any]:
    return dict((_deserialize(key), _deserialize(val)) for key, val in args)


def _dump_enum(instance: Enum) -> Serialized:
    return _serialize(instance, _dump(instance.value))


def _load_enum(factory: Callable[..., TVar]) -> Callable[..., TVar]:
    return lambda value: factory(_deserialize(value))


def _load_list(*args: Serialized) -> List[Any]:
    return list(_load_tuple(*args))


def _dump_named_tuple(instance: Tuple[Any, ...]) -> Serialized:
    return _serialize(instance, *map(_dump, instance))


def _load_named_tuple(factory: Callable[..., TVar]) -> Callable[..., TVar]:
    return lambda *args: factory(*map(_deserialize, args))


def _dump_none(instance: None) -> Serialized:
    return _serialize(instance)


def _load_none() -> None:
    return None


def _load_ordered_dict(*args: Tuple[Serialized, Serialized]) -> Dict[Any, Any]:
    return OrderedDict(_load_dict(*args))


def _dump_tuple(instance: List[Any]) -> Serialized:
    return _serialize(instance, *map(_dump, instance))


def _load_tuple(*args: Serialized) -> Tuple[Any, ...]:
    return tuple(map(_deserialize, args))


def get_signature(factory: Any) -> Tuple[str, str]:
    return (factory.__module__, factory.__name__)


# This is what guarantees security, only this types are whitelisted
ALLOWED_FACTORIES: Dict[type, Dict[str, Any]] = {
    factory: dict(
        dumper=dumper,
        loader=loader,
        signature=get_signature(factory),
    )
    for _dump_base in [lambda x: _serialize(x, x)]
    for factory, dumper, loader in [
        (bytes, _dump_bytes, _load_bytes),
        (dict, _dump_dict, _load_dict),
        (float, _dump_base, float),
        (int, _dump_base, int),
        (list, _dump_tuple, _load_list),
        (OrderedDict, _dump_dict, _load_ordered_dict),
        (str, _dump_base, str),
        (tuple, _dump_tuple, _load_tuple),
        (type(None), _dump_none, _load_none),
        *[
            (enum, _dump_enum, _load_enum(enum))
            for enum in (
                FindingEnum,
                FindingTypeEnum,
                VulnerabilityApprovalStatusEnum,
                VulnerabilityKindEnum,
                VulnerabilitySourceEnum,
                VulnerabilityStateEnum,
            )
        ],
        *[
            (named_tuple, _dump_named_tuple, _load_named_tuple(named_tuple))
            for named_tuple in (
                FindingMetadata,
                IntegratesVulnerabilityMetadata,
                NVDVulnerability,
                SkimsVulnerabilityMetadata,
                Vulnerability,
            )
        ],
    ]
}
SIGNATURE_TO_FACTORY: Dict[Any, type] = {
    factory_attributes['signature']: factory
    for factory, factory_attributes in ALLOWED_FACTORIES.items()
}


def _serialize(
    instance: Any,
    *args: Any,
    **kwargs: Any,
) -> Serialized:
    signature = ALLOWED_FACTORIES[type(instance)]['signature']

    return (signature, args, kwargs)


def _deserialize(data: Serialized) -> Any:
    signature, args, kwargs = tuple(data[0]), data[1], data[2]
    factory: type = SIGNATURE_TO_FACTORY[signature]
    loader: Callable[..., Any] = ALLOWED_FACTORIES[factory]['loader']

    return loader(*args, **kwargs)


def _dump(instance: Any) -> Serialized:
    factory = type(instance)
    dumper: Callable[..., Serialized] = ALLOWED_FACTORIES[factory]['dumper']

    return dumper(instance)


async def dump(instance: Any, ttl: Optional[int] = None) -> bytes:
    dumped: Serialized = await in_process(_dump, instance)
    message = {
        'expires_at': None if ttl is None else get_utc_timestamp() + ttl,
        'instance': dumped,
    }

    serialized: str = (
        await in_process(json.dumps, message, separators=(',', ':'))
    )

    return await in_process(serialized.encode, 'utf-8')


async def load(stream: bytes) -> Any:
    try:
        deserialized: Any = await in_process(json.loads, stream)

        expires_at: Optional[int] = deserialized['expires_at']
        if expires_at and get_utc_timestamp() > expires_at:
            raise LoadError('Data has expired')

        return await in_process(_deserialize, deserialized['instance'])
    except (
        AttributeError,
        json.decoder.JSONDecodeError,
        LoadError,
        TypeError,
        ValueError,
    ) as exc:
        await log_exception('debug', exc)
        raise LoadError(exc)
