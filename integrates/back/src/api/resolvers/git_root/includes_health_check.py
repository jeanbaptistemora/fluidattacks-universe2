from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: GitRoot, _info: GraphQLResolveInfo) -> bool:
    return parent.state.includes_health_check
