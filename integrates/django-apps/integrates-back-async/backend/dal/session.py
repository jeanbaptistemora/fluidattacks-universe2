import base64
import json
from typing import Dict, List, Optional
from backend.dal.helpers.redis import REDIS_CLIENT


def deserialize(session_key: str):
    return json.loads(
        ':'.join(
            base64.b64decode(REDIS_CLIENT.get(session_key))
            .decode('utf-8')
            .split(':')[1:]
        )
    )


def get_all_logged_users() -> List[Dict[str, str]]:
    """ returns a user : session_key array for each active redis session"""
    sessions_values_usernames = [
        {
            'key': key,
            **deserialize(key)
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
    current_session = deserialize(f'fi_session:{session_key}')
    old_session_key = [
        session
        for session in all_active_sessions
        if session['username'] == user_mail
        and session['client'] == current_session.get('client', 'web')
        and session['key'] != f'fi_session:{session_key}'
    ]
    return old_session_key[0]['key'] if old_session_key else None


def invalidate_session(session_key: str):
    REDIS_CLIENT.delete(session_key)


def add_element(key: str, value: str, time: int):
    REDIS_CLIENT.setex(key, time, value)


def remove_element(key: str):
    REDIS_CLIENT.delete(key)


def element_exists(key: str) -> bool:
    return REDIS_CLIENT.get(key)
