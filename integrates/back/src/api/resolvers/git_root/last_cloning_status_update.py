from db_model.roots.types import (
    GitRootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: GitRootItem, _info: GraphQLResolveInfo) -> str:
    return parent.cloning.modified_date
