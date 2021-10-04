from ariadne import (
    UnionType,
)
from graphql.type.definition import (
    GraphQLAbstractType,
    GraphQLResolveInfo,
)
from roots.types import (
    GitRoot,
    IPRoot,
    Root,
    URLRoot,
)
from typing import (
    Optional,
    Tuple,
)


def resolve_root_type(
    result: Root, _info: GraphQLResolveInfo, _return_type: GraphQLAbstractType
) -> Optional[str]:
    # pylint: disable=unsubscriptable-object
    if isinstance(result, GitRoot):
        return "GitRoot"
    if isinstance(result, IPRoot):
        return "IPRoot"
    if isinstance(result, URLRoot):
        return "URLRoot"
    return None


UNIONS: Tuple[UnionType, ...] = (UnionType("Root", resolve_root_type),)
