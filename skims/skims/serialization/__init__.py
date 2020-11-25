# Standard libraries
from collections import (
    OrderedDict,
)
from enum import (
    Enum,
)
import json
from datetime import (
    datetime,
    date,
)

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
from dateutil.parser import (
    parse as date_parser
)
from lark import (
    Tree as LarkTree,
)
from lark.tree import (
    Meta as LarkMeta,
)
from metaloaders.model import (
    Node,
    Type,
)
import networkx as nx

# Local libraries
from parse_common.types import (
    ListToken,
)
from parse_hcl2.tokens import (
    Attribute as HCL2Attribute,
    Block as HCL2Block,
    Json as HCL2Json,
)
from utils.graph import (
    export_graph_as_json,
    import_graph_from_json,
)
from utils.logs import (
    log_exception,
)
from utils.model import (
    FindingEnum,
    FindingMetadata,
    FindingTypeEnum,
    Grammar,
    IntegratesVulnerabilityMetadata,
    NVDVulnerability,
    Platform,
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


def _dump_datetime(time: datetime) -> Serialized:
    return _serialize(time, time.isoformat())


def _load_datetime(time: str) -> datetime:
    return date_parser(time)


def _load_dict(*args: Tuple[Serialized, Serialized]) -> Dict[Any, Any]:
    return dict((_deserialize(key), _deserialize(val)) for key, val in args)


def _dump_enum(instance: Enum) -> Serialized:
    return _serialize(instance, _dump(instance.value))


def _load_enum(factory: Callable[..., TVar]) -> Callable[..., TVar]:
    return lambda value: factory(_deserialize(value))


def _dump_graph(instance: nx.OrderedDiGraph) -> Serialized:
    graph_as_json = export_graph_as_json(instance, include_styles=True)
    return _serialize(instance, graph_as_json)


def _load_graph(graph_as_json: Any) -> nx.OrderedDiGraph:
    return import_graph_from_json(graph_as_json)


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


def _dump_lark_meta(meta: LarkMeta) -> Serialized:
    return _serialize(meta, *map(_dump, {
        attr: getattr(meta, attr, None)
        for attr in ('column', 'empty', 'end_column', 'end_line', 'line')
    }))


def _load_lark_meta(**kwargs: Any) -> LarkMeta:
    meta = LarkMeta()
    for attr, value in kwargs.items():
        if value is not None:
            setattr(meta, attr, value)
    return meta


def _dump_lark_tree(tree: LarkTree) -> Serialized:
    return _serialize(tree, *map(_dump, (tree.children, tree.data, tree.meta)))


def _load_lark_tree(children: Any, data: Any, meta: Any) -> LarkTree:
    return LarkTree(data, children, meta)


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
        (bool, _dump_base, bool),
        (bytes, _dump_bytes, _load_bytes),
        (dict, _dump_dict, _load_dict),
        (date, _dump_datetime, _load_datetime),
        (datetime, _dump_datetime, _load_datetime),
        (float, _dump_base, float),
        (int, _dump_base, int),
        (list, _dump_tuple, _load_list),
        (LarkMeta, _dump_lark_meta, _load_lark_meta),
        (LarkTree, _dump_lark_tree, _load_lark_tree),
        (ListToken, _dump_tuple, _load_list),
        (nx.OrderedDiGraph, _dump_graph, _load_graph),
        (OrderedDict, _dump_dict, _load_ordered_dict),
        (str, _dump_base, str),
        (tuple, _dump_tuple, _load_tuple),
        (type(None), _dump_none, _load_none),
        *[
            (enum, _dump_enum, _load_enum(enum))
            for enum in (
                FindingEnum,
                FindingTypeEnum,
                Grammar,
                Platform,
                VulnerabilityApprovalStatusEnum,
                VulnerabilityKindEnum,
                VulnerabilitySourceEnum,
                VulnerabilityStateEnum,
                Type,
            )
        ],
        *[
            (named_tuple, _dump_named_tuple, _load_named_tuple(named_tuple))
            for named_tuple in (
                FindingMetadata,
                HCL2Attribute,
                HCL2Block,
                HCL2Json,
                IntegratesVulnerabilityMetadata,
                NVDVulnerability,
                SkimsVulnerabilityMetadata,
                Vulnerability,
                Node
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
