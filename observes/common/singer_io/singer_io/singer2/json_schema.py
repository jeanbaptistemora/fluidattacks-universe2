# pylint: skip-file
from dataclasses import (
    dataclass,
)
from jsonschema import (
    Draft4Validator,
)
from jsonschema.exceptions import (
    ValidationError,
)
from returns.result import (
    Failure,
    Result,
    Success,
)
from typing import (
    Any,
    Dict,
)


@dataclass(frozen=True)
class _JsonSchema:
    raw_schema: Dict[str, Any]
    validator: Draft4Validator


@dataclass(frozen=True)
class JsonSchema(_JsonSchema):
    def __init__(self, obj: _JsonSchema) -> None:
        for key, value in obj.__dict__.items():
            object.__setattr__(self, key, value)

    def validate(
        self, raw_record: Dict[str, Any]
    ) -> Result[None, ValidationError]:
        try:
            self.validator.validate(raw_record)
            return Success(None)
        except ValidationError as error:
            return Failure(error)


def jschema_from_raw(raw_schema: Dict[str, Any]) -> JsonSchema:
    Draft4Validator.check_schema(raw_schema)
    validator = Draft4Validator(raw_schema)
    draft = _JsonSchema(raw_schema, validator)
    return JsonSchema(draft)
