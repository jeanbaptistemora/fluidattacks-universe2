# Standard
from typing import Dict

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import require_login
from backend.typing import Me


@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Me:
    caller_origin: str = kwargs.get('caller_origin', 'API')
    user_data: Dict[str, str] = await util.get_jwt_content(info.context)

    return {
        'caller_origin': caller_origin,
        'session_expiration': user_data['exp'],
        'user_email': user_data['user_email']
    }
