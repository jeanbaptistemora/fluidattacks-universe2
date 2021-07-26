from dataclasses import (
    dataclass,
)
from jsonschema import (
    Draft4Validator,
)
from typing import (
    Any,
    Dict,
)


@dataclass(frozen=True)
class JsonSchema:
    raw_schema: Dict[str, Any]

    def __init__(self, raw_schema: Dict[str, Any]) -> None:
        Draft4Validator.check_schema(raw_schema)
        object.__setattr__(self, "raw_schema", raw_schema)
