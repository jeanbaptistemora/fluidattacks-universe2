from db_model.roots.types import (
    GitRootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


def resolve(parent: GitRootItem, _info: GraphQLResolveInfo) -> dict[str, Any]:
    return {
        "commit": parent.cloning.commit,
        "message": parent.cloning.reason,
        "status": parent.cloning.status.value,
    }
