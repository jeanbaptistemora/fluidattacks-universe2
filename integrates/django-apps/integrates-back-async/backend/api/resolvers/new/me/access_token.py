# Standard
import json
from typing import cast, Dict, Optional

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.domain import user as user_domain
from backend.typing import Me


async def resolve(
    _parent: Me,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    user_data: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']
    access_token: Optional[Dict[str, str]] = cast(
        Optional[Dict[str, str]],
        await user_domain.get_data(
            user_email,
            'access_token'
        )
    )

    return json.dumps({
        'hasAccessToken': bool(access_token),
        'issuedAt': (
            str(access_token.get('iat', ''))
            if isinstance(access_token, dict)
            else ''
        )
    })
