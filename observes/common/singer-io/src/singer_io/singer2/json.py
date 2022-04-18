from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from deprecated import (  # type: ignore
    deprecated,
)
import json
from json.encoder import (
    JSONEncoder,
)
from purity.v1 import (
    DictFactory,
    InvalidType,
    JsonFactory,
    JsonObj,
    JsonValFactory,
    JsonValue,
    Primitive,
    PrimitiveFactory,
    PrimitiveTypes,
    UnexpectedResult,
)
from returns.io import (
    IO,
)
import sys
from typing import (
    Any,
    IO as IO_FILE,
)

to_primitive = deprecated(reason="use purity.v1.PrimitiveFactory")(
    PrimitiveFactory.to_primitive
)
to_opt_primitive = deprecated(reason="use purity.v1.PrimitiveFactory")(
    PrimitiveFactory.to_opt_primitive
)


class CustomJsonEncoder(JSONEncoder):
    def default(self: JSONEncoder, o: Any) -> Any:
        if isinstance(o, JsonValue):
            return o.unfold()
        return JSONEncoder.default(self, o)


@dataclass(frozen=True)
class JsonEmitter:
    # pylint: disable=no-self-use
    target: IO_FILE[str] = sys.stdout

    def to_str(self, json_obj: JsonObj, **kargs: Any) -> str:
        return json.dumps(json_obj, cls=CustomJsonEncoder, **kargs)

    def emit(self, json_obj: JsonObj) -> IO[None]:
        json.dump(json_obj, self.target, cls=CustomJsonEncoder)
        self.target.write("\n")
        return IO(None)


__all__ = [
    "Primitive",
    "PrimitiveTypes",
    "InvalidType",
    "JsonValue",
    "JsonObj",
    "UnexpectedResult",
    "DictFactory",
    "JsonValFactory",
    "JsonFactory",
]
