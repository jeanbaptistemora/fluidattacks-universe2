# Standard libraries
import contextlib
import json
from typing import (
    Any,
    Dict,
    Optional,
)

# Third-party libraries
from aioextensions import collect
from starlette.requests import Request

# Local libraries
from back import settings
from backend import authz
from backend.exceptions import (
    ExpiredToken,
    SecureAccessException,
)
from redis_cluster.model import KeyNotFound as RedisKeyNotFound
from redis_cluster.operations import (
    redis_cmd,
    redis_del_by_deps,
    redis_del_entity_attr,
    redis_get_entity_attr,
    redis_set_entity_attr,
)
from users import dal as users_dal


async def add_element(key: str, value: Dict[str, Any], time: int) -> None:
    await redis_cmd('setex', key, time, json.dumps(value))


async def check_jwt_token_validity(request: Request) -> None:
    email: str = request.session['username']
    attr: str = 'jwt'
    try:
        if await get_session_key(email, attr):
            # Jwt cookie are ok and up to date
            pass
        else:
            # Jwt cookie is expired, let's logout the user
            await remove_session_key(email, attr)
            request.session.clear()
            raise ExpiredToken()
    except RedisKeyNotFound:
        # User do not even has an active session
        raise SecureAccessException()


async def check_session_web_validity(request: Request) -> None:
    email: str = request.session['username']
    session_key: str = request.session['session_key']
    attr: str = 'web'

    # Check if the user has a concurrent session and in case they do
    # raise the concurrent session modal flag
    if request.session.get('is_concurrent'):
        request.session.pop('is_concurrent')
        await users_dal.update(email, {'is_concurrent_session': True})
    try:
        # Check if the user has an active session but it's different
        # than the one in the cookie
        if await get_session_key(email, attr) == session_key:
            # Session and cookie are ok and up to date
            pass
        else:
            # Session or the cookie are expired, let's logout the user
            await remove_session_key(email, attr)
            request.session.clear()
            raise ExpiredToken()
    except RedisKeyNotFound:
        # User do not even has an active session
        raise SecureAccessException()


async def create_session_web(request: Request) -> bool:
    email: str = request.session['username']
    session_key: str = request.session['session_key']

    # Check if there is a session already
    request.session['is_concurrent'] = bool(
        await get_session_key(email, 'web')
    )

    # Proccede overwritting the user session
    # This means that if a session did exist before, this one will
    # take place and the other will be removed
    return await redis_set_entity_attr(
        entity='session',
        attr='web',
        email=email,
        value=session_key,
        ttl=settings.SESSION_COOKIE_AGE,
    )


async def delete_user(email: str) -> bool:
    success = all(
        await collect([
            authz.revoke_user_level_role(email),
            users_dal.delete(email)
        ])
    )
    await logout(email)
    return success


async def get_session_key(email: str, attr: str) -> Optional[str]:
    session_key: Optional[str] = None
    with contextlib.suppress(RedisKeyNotFound):
        session_key = await redis_get_entity_attr(
            entity='session',
            attr=attr,
            email=email,
        )
    return session_key


async def logout(email: str) -> None:
    await redis_del_by_deps('session_logout', session_email=email)


async def remove_session_key(email: str, attr: str) -> bool:
    return await redis_del_entity_attr(
        entity='session',
        attr=attr,
        email=email,
    )
