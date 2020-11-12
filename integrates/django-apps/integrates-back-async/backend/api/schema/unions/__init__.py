# Standard
from typing import Optional, Tuple

# Third party
from ariadne import UnionType
from graphql.type.definition import GraphQLAbstractType, GraphQLResolveInfo

# Local
from backend.typing import Root


def resolve_root_type(
    result: Root,
    _info: GraphQLResolveInfo,
    _return_type: GraphQLAbstractType
) -> Optional[str]:
    if result.kind == 'Git':
        return 'GitRoot'
    if result.kind == 'IP':
        return 'IPRoot'
    if result.kind == 'URL':
        return 'URLRoot'

    return None


UNIONS: Tuple[UnionType, ...] = (
    UnionType('Root', resolve_root_type),
)
