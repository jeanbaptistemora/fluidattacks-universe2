import base64
import json
from typing import (
    Awaitable,
    Dict,
    List,
    Optional,
)

from aioextensions import (
    collect,
)
from backend.dal.helpers.redis import (
    AREDIS_CLIENT,
    REDIS_CLIENT,
)


async def deserialize(session_key: str):
    return json.loads(
        ':'.join(
            base64.b64decode(await AREDIS_CLIENT.get(session_key))
            .decode('utf-8')
            .split(':')[1:]
        )
    )


async def get_all_logged_users() -> List[Dict[str, str]]:
    """ returns a user : session_key array for each active redis session"""
    coroutines: List[Awaitable[dict]] = []
    keys = []
    async for key in AREDIS_CLIENT.scan_iter('fi_session:*'):
        coroutines.append(deserialize(key))
        keys.append(key)
    dicts_deserialized = await collect(coroutines)

    return [
        {
            'key': key,
            **deserialized
        }
        for deserialized, key in zip(dicts_deserialized, keys)
    ]


async def get_previous_session(
        user_mail: str, session_key: str) -> Optional[str]:
    """
    checks if exists other active session with
    the same user_mail and if so returns it
    """
    all_active_sessions = await get_all_logged_users()
    current_session = await deserialize(f'fi_session:{session_key}')
    old_session_key = [
        session
        for session in all_active_sessions
        if session.get('username') == user_mail
        and session.get('client') == current_session.get('client', 'web')
        and session['key'] != f'fi_session:{session_key}'
    ]
    return old_session_key[0]['key'] if old_session_key else None


async def invalidate_session(session_key: str):
    await AREDIS_CLIENT.delete(session_key)


async def add_element(key: str, value: str, time: int):
    await AREDIS_CLIENT.setex(key, time, value)


async def remove_element(key: str):
    await AREDIS_CLIENT.delete(key)


def element_exists(key: str) -> bool:
    return REDIS_CLIENT.get(key)
