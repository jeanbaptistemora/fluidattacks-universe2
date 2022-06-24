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
        first_login = parent.get("first_login", None)
    else:
        first_login = (
            convert_from_iso_str(parent.registration_date)
            if parent.registration_date
            else None
        )
    return first_login
