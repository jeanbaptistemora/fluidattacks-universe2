from ariadne import (
    ScalarType,
)
from graphql.language.ast import (
    BooleanValueNode,
    FloatValueNode,
    IntValueNode,
    ListValueNode,
    ObjectValueNode,
    StringValueNode,
)
from typing import (
    Any,
    TypeVar,
)

GENERIC_SCALAR = ScalarType("GenericScalar")
T = TypeVar("T")


@GENERIC_SCALAR.serializer
def serialize_genericscalar(value: T) -> T:
    return value


@GENERIC_SCALAR.value_parser
def parse_genericscalar_value(value: T) -> T:
    return value


@GENERIC_SCALAR.literal_parser  # type: ignore
def parse_genericscalar_literal(ast: Any) -> Any:
    if isinstance(ast, (StringValueNode, BooleanValueNode)):
        return ast.value
    if isinstance(ast, IntValueNode):
        return int(ast.value)
    if isinstance(ast, FloatValueNode):
        return float(ast.value)
    if isinstance(ast, ListValueNode):
        return [
            parse_genericscalar_literal(value)  # type: ignore
            for value in ast.values
        ]
    if isinstance(ast, ObjectValueNode):
        return {
            field.name.value: parse_genericscalar_literal(
                field.value  # type: ignore
            )
            for field in ast.fields
        }
    return None
