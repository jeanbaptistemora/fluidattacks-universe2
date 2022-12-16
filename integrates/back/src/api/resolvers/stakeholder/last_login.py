from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Stakeholder,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    return (
        datetime_utils.get_as_utc_iso_format(parent.last_login_date)
        if parent.last_login_date
        else None
    )
