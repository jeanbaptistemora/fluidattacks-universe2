from .schema import (
    ME,
)
from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import json
from newutils.datetime import (
    get_as_utc_iso_format,
)
from stakeholders.domain import (
    get_stakeholder,
)
from typing import (
    Any,
)


@ME.field("accessToken")
async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    user_email = str(parent["user_email"])
    loaders: Dataloaders = info.context.loaders
    stakeholder: Stakeholder = await get_stakeholder(loaders, user_email)
    access_token = stakeholder.access_token

    return json.dumps(
        {
            "hasAccessToken": bool(access_token),
            "issuedAt": (
                str(access_token.iat) if access_token is not None else ""
            ),
            "lastAccessTokenUse": None
            if stakeholder.last_api_token_use_date is None
            else get_as_utc_iso_format(stakeholder.last_api_token_use_date),
        }
    )
