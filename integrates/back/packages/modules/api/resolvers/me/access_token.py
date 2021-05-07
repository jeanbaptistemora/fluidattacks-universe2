# Standard
import json
from typing import (
    Dict,
    Optional,
    cast,
)

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import Me
from users import domain as users_domain


async def resolve(
    parent: Me,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    user_email: str = cast(str, parent['user_email'])
    access_token: Optional[Dict[str, str]] = cast(
        Optional[Dict[str, str]],
        await users_domain.get_data(user_email, 'access_token')
    )
    return json.dumps({
        'hasAccessToken': bool(access_token),
        'issuedAt': (
            str(access_token.get('iat', ''))
            if isinstance(access_token, dict)
            else ''
        )
    })
