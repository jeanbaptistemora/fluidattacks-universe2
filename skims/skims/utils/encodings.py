# Standard library
import dataclasses
from enum import Enum
import json
from typing import (
    Any,
)

# Third party libraries
from ruamel import yaml
from aioextensions import (
    in_thread,
)

# Local libraries
from utils.graph import (
    export_graph_as_json,
)
from model import (
    core_model,
    graph_model,
)


def simplify(obj: Any) -> Any:
    simplified_obj: Any
    if hasattr(obj, "_fields"):
        # NamedTuple
        simplified_obj = dict(
            zip(
                simplify(obj._fields),
                simplify(tuple(obj)),
            )
        )
    elif isinstance(obj, Enum):
        simplified_obj = obj.value
    elif isinstance(obj, dict):
        simplified_obj = dict(
            zip(
                simplify(tuple(obj.keys())),
                simplify(tuple(obj.values())),
            )
        )
    elif isinstance(obj, (list, tuple, set)):
        simplified_obj = tuple(map(simplify, obj))
    elif isinstance(obj, graph_model.Graph):
        simplified_obj = export_graph_as_json(obj)
    elif dataclasses.is_dataclass(obj):
        simplified_obj = simplify(dataclasses.asdict(obj))
    else:
        simplified_obj = obj

    return simplified_obj


def json_dump(element: object, *args: Any, **kwargs: Any) -> None:
    json.dump(simplify(element), *args, **kwargs)


def json_dumps(element: object, *args: Any, **kwargs: Any) -> str:
    return json.dumps(simplify(element), *args, **kwargs)


def yaml_dumps_blocking(element: object, *args: Any, **kwargs: Any) -> str:
    element = simplify(element)

    dumped: str = yaml.safe_dump(
        element,
        *args,
        default_flow_style=False,
        **kwargs,
    )

    return dumped


async def yaml_dumps(element: object, *args: Any, **kwargs: Any) -> str:
    element = simplify(element)

    return await in_thread(yaml_dumps_blocking, element, *args, **kwargs)


def deserialize_namespace_from_vuln(
    kind: core_model.VulnerabilityKindEnum,
    what: str,
) -> str:
    namespace: str

    if kind == core_model.VulnerabilityKindEnum.INPUTS:
        namespace = what.rsplit(" (", maxsplit=1)[0][:-1]
    elif kind == core_model.VulnerabilityKindEnum.LINES:
        namespace = what.split("/", maxsplit=1)[0]
    elif kind == core_model.VulnerabilityKindEnum.PORTS:
        namespace = what.rsplit(" (", maxsplit=1)[0][:-1]
    else:
        raise NotImplementedError()

    return namespace


def deserialize_what_from_vuln(
    kind: core_model.VulnerabilityKindEnum,
    what: str,
) -> str:
    if kind == core_model.VulnerabilityKindEnum.INPUTS:
        what = what.rsplit(" (", maxsplit=1)[1][:-1]
    elif kind == core_model.VulnerabilityKindEnum.LINES:
        what = what.split("/", maxsplit=1)[1]
    elif kind == core_model.VulnerabilityKindEnum.PORTS:
        what = what.rsplit(" (", maxsplit=1)[1][:-1]
    else:
        raise NotImplementedError()

    return what


def serialize_namespace_into_vuln(
    kind: core_model.VulnerabilityKindEnum,
    namespace: str,
    what: str,
) -> str:
    if kind == core_model.VulnerabilityKindEnum.INPUTS:
        what = f"{what} ({namespace})"
    elif kind == core_model.VulnerabilityKindEnum.LINES:
        what = f"{namespace}/{what}"
    elif kind == core_model.VulnerabilityKindEnum.PORTS:
        what = f"{what} ({namespace})"
    else:
        raise NotImplementedError()

    return what
