# Standard libraries
from datetime import datetime
from typing import Any

# Local libraries
from backend import util
from backend.exceptions import InvalidExpirationTime
from backend.typing import (
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
)
from newutils import token as token_utils
from users import dal as users_dal


async def remove_access_token(email: str) -> bool:
    """ Remove access token attribute """
    return await users_dal.update(email, {'access_token': None})


async def update_access_token(
    email: str,
    expiration_time: int,
    **kwargs_token: Any
) -> UpdateAccessTokenPayloadType:
    """ Update access token """
    token_data = util.calculate_hash_token()
    session_jwt = ''
    success = False

    if util.is_valid_expiration_time(expiration_time):
        iat = int(datetime.utcnow().timestamp())
        session_jwt = token_utils.new_encoded_jwt(
            {
                'user_email': email,
                'jti': token_data['jti'],
                'iat': iat,
                'exp': expiration_time,
                'sub': 'api_token',
                **kwargs_token
            },
            api=True
        )
        access_token = {
            'iat': iat,
            'jti': token_data['jti_hashed'],
            'salt': token_data['salt']
        }
        success = await users_dal.update(email, {'access_token': access_token})
    else:
        raise InvalidExpirationTime()

    return UpdateAccessTokenPayloadType(
        success=success,
        session_jwt=session_jwt
    )
