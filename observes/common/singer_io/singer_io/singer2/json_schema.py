# pylint: skip-file
from dataclasses import (
    dataclass,
    field,
)
from enum import (
    Enum,
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
    JsonValue,
    PrimitiveTypes,
)
from typing import (
    Any,
    Dict,
)


class SupportedType(Enum):
    array = "array"
    boolean = "boolean"
    integer = "integer"
    null = "null"
    number = "number"
    object = "object"
    string = "string"


@dataclass(frozen=True)
class _JsonSchema:
    raw_schema: Dict[str, Any]
    validator: Draft4Validator = field(compare=False)


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
    @staticmethod
    def from_dict(raw_dict: Dict[str, Any]) -> JsonSchema:
        Draft4Validator.check_schema(raw_dict)
        validator = Draft4Validator(raw_dict)
        draft = _JsonSchema(raw_dict, validator)
        return JsonSchema(draft)

    @classmethod
    def from_raw(cls, raw_schema: str) -> JsonSchema:
        raw = DictFactory.loads(raw_schema)
        return cls.from_dict(raw)

    @classmethod
    def from_json(cls, json_obj: JsonObj) -> JsonSchema:
        raw = DictFactory.from_json(json_obj)
        return cls.from_dict(raw)

    @classmethod
    def from_prim_type(cls, ptype: PrimitiveTypes) -> JsonSchema:
        encode_type = {
            bool: SupportedType.boolean,
            int: SupportedType.integer,
            type(None): SupportedType.null,
            float: SupportedType.number,
            str: SupportedType.string,
        }
        return JsonSchema(
            cls.from_json({"type": JsonValue(encode_type[ptype].value)})
        )
