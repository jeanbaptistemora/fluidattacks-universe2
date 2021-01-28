# Standard libraries
import contextlib
from typing import (
    Any,
    cast,
    Dict,
    Optional,
)
import simplejson as json

# Third party libraries
from starlette.requests import (
    Request,
)

# Local libraries
from back import settings
from backend.model import (
    redis_model,
)
from backend.dal.helpers.redis import (
    redis_cmd,
    redis_del_entity_attr,
    redis_get_entity_attr,
    redis_set_entity_attr,
)
from backend.exceptions import (
    ConcurrentSession,
    ExpiredToken,
    SecureAccessException,
)


async def create_session_web(request: Request) -> bool:
    email: str = request.session['username']
    session_key: str = request.session['session_key']

    # Check if there is a session already
    request.session['is_concurrent'] = bool(await get_session_web(email))

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


async def remove_session_web(email: str) -> bool:
    return await redis_del_entity_attr(
        entity='session',
        attr='web',
        email=email,
    )


async def get_session_web(email: str) -> Optional[str]:
    session_key: Optional[str] = None

    with contextlib.suppress(redis_model.KeyNotFound):
        session_key = await redis_get_entity_attr(
            entity='session',
            attr='web',
            email=email,
        )

    return session_key


async def check_session_web_validity(request: Request) -> None:
    email: str = request.session['username']
    session_key: str = request.session['session_key']

    # Check if the user has a concurrent session
    if request.session.get('is_concurrent'):
        request.session.pop('is_concurrent')
        raise ConcurrentSession()

    try:
        # Check if the user has an active session but it's different
        # than the one in the cookie
        if await get_session_web(email) == session_key:
            # Session and cookie are ok and up to date
            pass
        else:
            # Session or the cookie are expired, let's logout the user
            await remove_session_web(email)
            request.session.clear()
            raise ExpiredToken()
    except redis_model.KeyNotFound:
        # Use do not even has an active session
        raise SecureAccessException()


async def add_element(key: str, value: Dict[str, Any], time: int) -> None:
    await redis_cmd('setex', key, time, json.dumps(value))


async def element_exists(key: str) -> bool:
    return cast(
        bool,
        await redis_cmd('exists', key) > 0
    )
