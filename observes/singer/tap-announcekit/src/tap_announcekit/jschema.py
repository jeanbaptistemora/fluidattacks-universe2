from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from singer_io.singer2.json import (
    JsonObj,
    JsonValFactory,
    JsonValue,
)
from singer_io.singer2.json_schema import (
    JsonSchema,
    JsonSchemaFactory,
    SupportedType,
)
from typing import (
    Any,
    Dict,
    get_args,
    get_origin,
    Type,
    Union,
)


class UnexpectedType(Exception):
    pass


class UnsupportedMultipleType(Exception):
    pass


@dataclass(frozen=True)
class ObjEncoder:
    custom_map: Dict[Type[Any], JsonObj]

    def _to_jschema(self, ptype: Type[Any]) -> JsonObj:
        if ptype in self.custom_map.keys():
            return self.custom_map[ptype]
        if ptype in (datetime,):
            return JsonSchemaFactory.datetime_schema().to_json()
        return JsonSchemaFactory.from_prim_type(ptype).to_json()

    def _to_jschema_optional(
        self, ptype: Type[Any], optional: bool
    ) -> JsonObj:
        jschema = self._to_jschema(ptype).copy()
        if optional:
            jschema["type"] = JsonValFactory.from_list(
                [jschema["type"].to_primitive(str), SupportedType.null.value]
            )
        return jschema

    def _to_jschema_type(self, ptype: Type[Any]) -> JsonObj:
        if get_origin(ptype) is Union:
            var_types = get_args(ptype)
            single_type = list(
                filter(lambda x: not isinstance(None, x), var_types)
            )
            if len(single_type) > 1:
                raise UnsupportedMultipleType(single_type)
            return self._to_jschema_optional(
                single_type[0], type(None) in var_types
            )
        return self._to_jschema_optional(ptype, False)

    def to_jschema(self, obj_props: Dict[str, Type[Any]]) -> JsonSchema:
        props = {
            key: JsonValue(self._to_jschema_type(field_type))
            for key, field_type in obj_props.items()
        }
        return JsonSchemaFactory.from_json({"properties": JsonValue(props)})
