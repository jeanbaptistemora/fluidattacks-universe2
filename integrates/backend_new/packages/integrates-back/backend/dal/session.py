from typing import Dict

from backend.dal.helpers.redis import (
    AREDIS_CLIENT,
)


async def invalidate_session(session_key: str):
    await AREDIS_CLIENT.delete(session_key)


async def hset_element(name: str, key: str, value: str) -> None:
    await AREDIS_CLIENT.hset(name, key, value)


async def hgetall_element(name: str) -> Dict[str, str]:
    return await AREDIS_CLIENT.hgetall(name)


async def hdel_element(name: str, keys: str) -> None:
    return await AREDIS_CLIENT.hdel(name, keys)


async def add_element(key: str, value: str, time: int):
    await AREDIS_CLIENT.setex(key, time, value)


async def remove_element(key: str):
    await AREDIS_CLIENT.delete(key)


async def element_exists(key: str) -> bool:
    return bool(await AREDIS_CLIENT.get(key))
