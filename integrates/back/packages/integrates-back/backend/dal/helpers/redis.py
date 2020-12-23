# Redis related methods & declarations

# Standard libraries
from typing import (
    Any,
    Dict,
    Optional
)

# Third party libraries
import simplejson as json

from aredis import (
    StrictRedis as AStrictRedis,
    StrictRedisCluster as AStrictRedisCluster,
)

# Local libraries
from __init__ import FI_ENVIRONMENT, FI_REDIS_SERVER


CLIENT_CONFIG = {
    'host': FI_REDIS_SERVER,
    'port': 6379,
    'decode_responses': True,
    'max_connections': 2048,
}
if FI_ENVIRONMENT == 'development':
    AREDIS_CLIENT = AStrictRedis(
        **CLIENT_CONFIG,
        db=0,
    )
else:
    AREDIS_CLIENT = AStrictRedisCluster(
        **CLIENT_CONFIG,
        skip_full_coverage_check=True,
    )


async def exists(key: str) -> bool:
    return bool(await AREDIS_CLIENT.get(key))


async def hset(name: str, key: str, value: str) -> None:
    await AREDIS_CLIENT.hset(name, key, value)


async def hgetall(name: str) -> Dict[str, str]:
    return await AREDIS_CLIENT.hgetall(name)


async def hdel(name: str, keys: str) -> None:
    return await AREDIS_CLIENT.hdel(name, keys)


async def set_ttl(name: str, ttl: int) -> None:
    await AREDIS_CLIENT.expire(name, ttl)


async def get_ttl(key: str) -> int:
    return await AREDIS_CLIENT.ttl(key)


async def add(key: str, value: Any, ttl: int) -> None:
    await AREDIS_CLIENT.setex(key, ttl, json.dumps(value))


async def get(key: str) -> Optional[Any]:
    element = await AREDIS_CLIENT.get(key)
    if element is not None:
        element = json.loads(element)

    return element


async def delete(pattern: str) -> int:
    keys = [key async for key in AREDIS_CLIENT.scan_iter(match=pattern)]
    if keys:
        await AREDIS_CLIENT.delete(*keys)
    return len(keys)
