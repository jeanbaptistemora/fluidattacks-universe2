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
    update_date = parent.unreliable_indicators.unreliable_last_status_update
    if not update_date:
        return ""

    return datetime_utils.get_as_str(update_date)
