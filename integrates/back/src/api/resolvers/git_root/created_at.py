from datetime import (
    datetime,
)
from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(parent: GitRoot, _info: GraphQLResolveInfo) -> datetime:
    return parent.created_date
