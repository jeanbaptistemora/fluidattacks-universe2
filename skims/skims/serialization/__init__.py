# Standard libraries
from collections import (
    OrderedDict,
)
import dataclasses
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

# Local libraries
from model import (
    core_model,
    graph_model,
)
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
    log_exception_blocking,
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


def _dump_graph(instance: graph_model.Graph) -> Serialized:
    graph_as_json = export_graph_as_json(instance, include_styles=True)
    return _serialize(instance, graph_as_json)


def _load_graph(graph_as_json: Any) -> graph_model.Graph:
    return import_graph_from_json(graph_as_json)


def _load_list(*args: Serialized) -> List[Any]:
    return list(_load_tuple(*args))


def _dump_named_tuple(instance: Tuple[Any, ...]) -> Serialized:
    return _serialize(instance, *map(_dump, instance))


def _load_named_tuple(factory: Callable[..., TVar]) -> Callable[..., TVar]:
    return lambda *args: factory(*map(_deserialize, args))


def _dump_dataclass(instance: Any) -> Serialized:
    return _serialize(instance, *map(_dump, dataclasses.astuple(instance)))


def _load_dataclass(factory: Callable[..., TVar]) -> Callable[..., TVar]:
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
        (graph_model.Graph, _dump_graph, _load_graph),
        (ListToken, _dump_tuple, _load_list),
        (OrderedDict, _dump_dict, _load_ordered_dict),
        (str, _dump_base, str),
        (tuple, _dump_tuple, _load_tuple),
        (type(None), _dump_none, _load_none),
        *[
            (enum, _dump_enum, _load_enum(enum))
            for enum in (
                core_model.FindingEnum,
                core_model.FindingTypeEnum,
                core_model.Grammar,
                core_model.Platform,
                core_model.VulnerabilityApprovalStatusEnum,
                core_model.VulnerabilityKindEnum,
                core_model.VulnerabilitySourceEnum,
                core_model.VulnerabilityStateEnum,
                graph_model.GraphShardMetadataLanguage,
                Type,
            )
        ],
        *[
            (named_tuple, _dump_named_tuple, _load_named_tuple(named_tuple))
            for named_tuple in (
                core_model.FindingMetadata,
                HCL2Attribute,
                HCL2Block,
                HCL2Json,
                core_model.IntegratesVulnerabilityMetadata,
                core_model.NVDVulnerability,
                graph_model.GraphDB,
                graph_model.GraphShardCacheable,
                graph_model.GraphShard,
                graph_model.GraphShardMetadata,
                graph_model.GraphShardMetadataJava,
                graph_model.GraphShardMetadataJavaClass,
                graph_model.GraphShardMetadataJavaClassMethod,
                graph_model.GraphShardMetadataNodes,
                graph_model.GraphVulnerabilityParameters,
                graph_model.SyntaxStepArrayAccess,
                graph_model.SyntaxStepArrayInstantiation,
                graph_model.SyntaxStepArrayInitialization,
                graph_model.SyntaxStepAssignment,
                graph_model.SyntaxStepBinaryExpression,
                graph_model.SyntaxStepDeclaration,
                graph_model.SyntaxStepIf,
                graph_model.SyntaxStepFor,
                graph_model.SyntaxStepLiteral,
                graph_model.SyntaxStepMethodInvocation,
                graph_model.SyntaxStepMethodInvocationChain,
                graph_model.SyntaxStepNoOp,
                graph_model.SyntaxStepObjectInstantiation,
                graph_model.SyntaxStepSwitch,
                graph_model.SyntaxStepSymbolLookup,
                graph_model.SyntaxStepUnaryExpression,
                core_model.SkimsVulnerabilityMetadata,
                core_model.Vulnerability,
                Node,
            )
        ],
        *[
            (dataclass, _dump_dataclass, _load_dataclass(dataclass))
            for dataclass in (
                graph_model.SyntaxStepMeta,
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


def dump(instance: Any, ttl: Optional[int] = None) -> bytes:
    dumped: Serialized = _dump(instance)
    message = {
        'expires_at': None if ttl is None else get_utc_timestamp() + ttl,
        'instance': dumped,
    }

    serialized: str = json.dumps(message, separators=(',', ':'))

    return serialized.encode('utf-8')


def load(stream: bytes) -> Any:
    try:
        deserialized: Any = json.loads(stream)

        expires_at: Optional[int] = deserialized['expires_at']
        if expires_at and get_utc_timestamp() > expires_at:
            raise LoadError('Data has expired')

        return _deserialize(deserialized['instance'])
    except (
        AttributeError,
        json.decoder.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        log_exception_blocking('debug', exc)
        raise LoadError(exc)
