# Standard libraries
from typing import (
    Any,
    cast,
    Dict,
    Optional,
)
import simplejson as json

# Local libraries
from backend.dal.helpers.redis import (
    redis_cmd,
)
from backend.exceptions import (
    ConcurrentSession,
    ExpiredToken,
)


async def save_session_token(
    key: str,
    token: str,
    name: str,
    ttl: int
) -> None:
    await hset_element(key, token, name)
    await set_element_ttl(name, ttl)


async def check_concurrent_sessions(email: str, session_key: str) -> None:
    """
    This method checks if current user
    already has an active session and if so, removes it
    """
    user_session_key = f'fi_session:{email}'
    user_session = await hgetall_element(user_session_key)
    user_session_keys = list(user_session.keys())
    if len(user_session_keys) > 1:
        await hdel_element(user_session_key, user_session_keys[0])
        raise ConcurrentSession()
    if user_session_keys and user_session_keys[0].split(':')[1] != session_key:
        raise ExpiredToken


async def hset_element(name: str, key: str, value: str) -> None:
    await redis_cmd('hset', name, key, value)


async def set_element_ttl(name: str, ttl: int) -> None:
    await redis_cmd('expire', name, ttl)


async def hgetall_element(name: str) -> Dict[str, str]:
    return cast(
        Dict[str, str],
        await redis_cmd('hgetall', name)
    )


async def get_redis_element(key: str) -> Optional[Any]:
    element = await redis_cmd('get', key)
    if element is not None:
        element = json.loads(element)
    return element


async def hdel_element(name: str, keys: str) -> Any:
    return await redis_cmd('hdel', name, keys)


async def add_element(key: str, value: Dict[str, Any], time: int) -> None:
    await redis_cmd('setex', key, time, json.dumps(value))


async def remove_element(key: str) -> None:
    await redis_cmd('delete', key)


async def element_exists(key: str) -> bool:
    return cast(
        bool,
        await redis_cmd('exists', key) > 0
    )
