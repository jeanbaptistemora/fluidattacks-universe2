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
from newutils.datetime import (
    convert_from_iso_str,
)
from typing import (
    Any,
    Dict,
    Optional,
    Union,
)


@require_asm
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    if isinstance(parent, dict):
        return parent["deletion_date"]

    if parent.state.status == GroupStateStatus.DELETED:
        return convert_from_iso_str(parent.state.modified_date)

    return None
