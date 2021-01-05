from typing import Any, TypeVar
from graphql.language.ast import (
    StringValueNode,
    BooleanValueNode,
    IntValueNode,
    FloatValueNode,
    ListValueNode,
    ObjectValueNode
)

from ariadne import ScalarType

GENERIC_SCALAR = ScalarType('GenericScalar')
TVar = TypeVar('TVar')


@GENERIC_SCALAR.serializer  # type: ignore
def serialize_genericscalar(value: TVar) -> TVar:
    return value


@GENERIC_SCALAR.value_parser  # type: ignore
def parse_genericscalar_value(value: TVar) -> TVar:
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
        return [parse_genericscalar_literal(value) for value in ast.values]
    if isinstance(ast, ObjectValueNode):
        return {
            field.name.value: parse_genericscalar_literal(field.value)
            for field in ast.fields
        }
    return None
