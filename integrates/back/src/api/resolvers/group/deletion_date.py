from .schema import (
    GROUP,
)
from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


@GROUP.field("deletionDate")
@require_asm
def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str | None:
    return (
        datetime_utils.get_as_str(parent.state.modified_date)
        if parent.state.status == GroupStateStatus.DELETED
        else None
    )
