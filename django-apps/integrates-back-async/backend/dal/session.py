import base64
import json
from typing import Dict, List, Optional
from backend.dal.helpers.redis import REDIS_CLIENT


def get_all_logged_users() -> List[Dict[str, str]]:
    """ returns a user : session_key array for each active redis session"""
    sessions_values_usernames = [
        {
            json.loads(
                ':'.join(
                    base64.b64decode(REDIS_CLIENT.get(key))
                    .decode('utf-8')
                    .split(':')[1:]
                )
            )
            .get('username'): key
        }
        for key in REDIS_CLIENT.scan_iter('fi_session:*')
    ]
    return sessions_values_usernames


def get_previous_session(user_mail: str, session_key: str) -> Optional[str]:
    """
    checks if exists other active session with
    the same user_mail and if so returns it
    """
    all_active_sessions = get_all_logged_users()
    old_session_key = [
        item[1]
        for item in [
            list(session_value.items())[0]
            for session_value in all_active_sessions
        ]
        if item[0] == user_mail and
        item[1] != f'fi_session:{session_key}'
    ]
    return old_session_key[0] if old_session_key else None


def invalidate_session(session_key: str):
    REDIS_CLIENT.delete(session_key)


def add_element(key: str, value: str, time: int):
    REDIS_CLIENT.setex(key, time, value)


def remove_element(key: str):
    REDIS_CLIENT.delete(key)
