# Standard library
from enum import Enum
import json
from typing import (
    Any,
)

# Third party libraries
from ruamel import yaml

# Local libraries
from utils.aio import (
    unblock,
)


async def simplify(obj: Any) -> Any:

    def _simplify(_obj: Any) -> Any:
        simplified_obj: Any
        if hasattr(_obj, '_fields'):
            # NamedTuple
            simplified_obj = dict(zip(
                _simplify(_obj._fields),
                _simplify(tuple(_obj)),
            ))
        elif isinstance(_obj, Enum):
            simplified_obj = _obj.value
        elif isinstance(_obj, dict):
            simplified_obj = dict(zip(
                _simplify(tuple(_obj.keys())),
                _simplify(tuple(_obj.values())),
            ))
        elif isinstance(_obj, (list, tuple, set)):
            simplified_obj = tuple(map(_simplify, _obj))
        else:
            simplified_obj = _obj

        return simplified_obj

    return await unblock(_simplify, obj)


async def json_dumps(element: object, **kwargs: Any) -> str:
    return await unblock(json.dumps, await simplify(element), **kwargs)


async def yaml_dumps(element: object, **kwargs: Any) -> str:
    element = await simplify(element)

    return await unblock(
        yaml.safe_dump,  # type: ignore
        element,
        default_flow_style=False,
        **kwargs,
    )
