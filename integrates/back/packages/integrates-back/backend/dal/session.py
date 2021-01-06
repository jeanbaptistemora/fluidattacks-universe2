from typing import Any, cast, Dict
import simplejson as json

from backend.dal.helpers.redis import (
    redis_cmd,
)


async def invalidate_session(session_key: str) -> None:
    await redis_cmd('delete', session_key)


async def hset_element(name: str, key: str, value: str) -> None:
    await redis_cmd('hset', name, key, value)


async def set_element_ttl(name: str, ttl: int) -> None:
    await redis_cmd('expire', name, ttl)


async def hgetall_element(name: str) -> Dict[str, str]:
    return cast(
        Dict[str, str],
        await redis_cmd('hgetall', name)
    )


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
