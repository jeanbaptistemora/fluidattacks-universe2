from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    convert_from_iso_str,
)
from typing import (
    Any,
    Optional,
    Union,
)


async def resolve(
    parent: Union[dict[str, Any], Stakeholder],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    if isinstance(parent, dict):
        last_login = parent.get("last_login", None)
    else:
        last_login = (
            convert_from_iso_str(parent.last_login_date)
            if parent.last_login_date
            else None
        )
    return last_login
