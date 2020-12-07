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


def simplify(obj: Any) -> Any:
    simplified_obj: Any
    if hasattr(obj, '_fields'):
        # NamedTuple
        simplified_obj = dict(zip(
            simplify(obj._fields),
            simplify(tuple(obj)),
        ))
    elif isinstance(obj, Enum):
        simplified_obj = obj.value
    elif isinstance(obj, dict):
        simplified_obj = dict(zip(
            simplify(tuple(obj.keys())),
            simplify(tuple(obj.values())),
        ))
    elif isinstance(obj, (list, tuple, set)):
        simplified_obj = tuple(map(simplify, obj))
    elif dataclasses.is_dataclass(obj):
        simplified_obj = simplify(dataclasses.asdict(obj))
    else:
        simplified_obj = obj

    return simplified_obj


def json_dump(element: object, *args: Any, **kwargs: Any) -> None:
    json.dump(simplify(element), *args, **kwargs)


def json_dumps(element: object, *args: Any, **kwargs: Any) -> str:
    return json.dumps(simplify(element), *args, **kwargs)


def blocking_yaml_dumps(element: object, *args: Any, **kwargs: Any) -> str:
    element = simplify(element)

    return yaml.safe_dump(  # type: ignore
        element,
        *args,
        default_flow_style=False,
        **kwargs,
    )


async def yaml_dumps(element: object, *args: Any, **kwargs: Any) -> str:
    element = simplify(element)

    return await in_thread(blocking_yaml_dumps, element, *args, **kwargs)
