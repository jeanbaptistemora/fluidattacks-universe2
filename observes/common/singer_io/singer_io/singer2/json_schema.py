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
from singer_io.singer2.json import (
    DictFactory,
    JsonFactory,
    JsonObj,
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

    def to_json(self) -> JsonObj:
        return JsonFactory.from_dict(self.raw_schema)

    def validate(
        self, raw_record: Dict[str, Any]
    ) -> Result[None, ValidationError]:
        try:
            self.validator.validate(raw_record)
            return Success(None)
        except ValidationError as error:
            return Failure(error)


@dataclass(frozen=True)
class JsonSchemaFactory:
    @classmethod
    def from_dict(cls, raw_dict: Dict[str, Any]) -> JsonSchema:
        Draft4Validator.check_schema(raw_dict)
        validator = Draft4Validator(raw_dict)
        draft = _JsonSchema(raw_dict, validator)
        return JsonSchema(draft)

    @classmethod
    def from_raw(cls, raw_schema: str) -> JsonSchema:
        raw = DictFactory.loads(raw_schema)
        return cls.from_dict(raw)
