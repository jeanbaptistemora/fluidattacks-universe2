from graphql.type.definition import (
    GraphQLResolveInfo,
)
import json
from stakeholders import (
    domain as stakeholders_domain,
)
from typing import (
    Any,
    cast,
    Dict,
    Optional,
)


async def resolve(
    parent: Dict[str, Any], _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    user_email = str(parent["user_email"])
    access_token: Optional[Dict[str, str]] = cast(
        Optional[Dict[str, str]],
        await stakeholders_domain.get_data(user_email, "access_token"),
    )
    return json.dumps(
        {
            "hasAccessToken": bool(access_token),
            "issuedAt": (
                str(access_token.get("iat", ""))
                if isinstance(access_token, dict)
                else ""
            ),
        }
    )
