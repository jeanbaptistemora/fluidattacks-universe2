
from typing import Dict

from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import Me
from decorators import require_login
from newutils import token as token_utils


@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Me:
    caller_origin: str = kwargs.get('caller_origin', 'API')
    user_data: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    return {
        'caller_origin': caller_origin,
        'session_expiration': user_data['exp'],
        'user_email': user_data['user_email'],
        'user_name': ' '.join([
            user_data.get('first_name', ''),
            user_data.get('last_name', '')
        ])
    }
