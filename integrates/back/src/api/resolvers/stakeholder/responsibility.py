from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access import (
    domain as group_access_domain,
)
from newutils import (
    token as token_utils,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    responsibility: str = ""
    request_store = token_utils.get_request_store(info.context)
    entity = request_store.get("entity")

    if entity == "GROUP":
        responsibility = await group_access_domain.get_responsibility(
            email=parent.email,
            group_name=request_store["group_name"],
            is_registered=parent.is_registered,
        )

    return responsibility if responsibility else None
