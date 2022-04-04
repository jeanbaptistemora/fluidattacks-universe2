import contextlib
from custom_exceptions import (
    ExpiredToken,
    SecureAccessException,
)
import json
from redis_cluster.model import (
    KeyNotFound as RedisKeyNotFound,
)
from redis_cluster.operations import (
    redis_cmd,
    redis_del_entity_attr,
    redis_get_entity_attr,
    redis_set_entity_attr,
)
from settings import (
    SESSION_COOKIE_AGE,
)
from starlette.requests import (
    Request,
)
from typing import (
    Any,
    Dict,
    Optional,
)


async def add_element(key: str, value: Dict[str, Any], time: int) -> None:
    await redis_cmd("setex", key, time, json.dumps(value))


async def check_jwt_token_validity(request: Request) -> None:
    email: str = request.session["username"]
    attr: str = "jwt"
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
        raise SecureAccessException() from None


async def create_session_web(request: Request) -> bool:
    email: str = request.session["username"]
    session_key: str = request.session["session_key"]

    # Check if there is a session already
    request.session["is_concurrent"] = bool(
        await get_session_key(email, "web")
    )

    # Proccede overwritting the user session
    # This means that if a session did exist before, this one will
    # take place and the other will be removed
    return await redis_set_entity_attr(
        entity="session",
        attr="web",
        email=email,
        value=session_key,
        ttl=SESSION_COOKIE_AGE,
    )


async def get_session_key(email: str, attr: str) -> Optional[str]:
    session_key: Optional[str] = None
    with contextlib.suppress(RedisKeyNotFound):
        session_key = await redis_get_entity_attr(
            entity="session",
            attr=attr,
            email=email,
        )
    return session_key


async def remove_session_key(email: str, attr: str) -> bool:
    return await redis_del_entity_attr(
        entity="session",
        attr=attr,
        email=email,
    )
