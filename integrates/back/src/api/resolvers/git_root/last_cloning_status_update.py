from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


def resolve(parent: GitRoot, _info: GraphQLResolveInfo) -> str:
    return datetime_utils.get_as_str(parent.cloning.modified_date)
