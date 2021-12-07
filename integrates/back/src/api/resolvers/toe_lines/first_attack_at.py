from db_model.toe_lines.types import (
    ToeLines,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


@enforce_group_level_auth_async
async def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return (
        datetime_utils.get_as_utc_iso_format(parent.first_attack_at)
        if parent.first_attack_at is not None
        else ""
    )
