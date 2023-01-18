from aioextensions import (
    in_thread,
)
import dataclasses
from enum import (
    Enum,
)
import json
from model import (
    graph_model,
)
from typing import (
    Any,
)
from utils.graph import (
    export_graph_as_json,
)
import yaml


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
