from typing import List, cast
from exponent_server_sdk import PushClient, PushMessage
from i18n import t

from backend.dal import user as user_dal


def notify_mobile(recipients: List[str], title: str, message: str):
    message += t('notifications.details')
    for user_email in recipients:
        user_devices = cast(List[str], user_dal.get_attributes(
            user_email, ['devices_to_notify']).get('devices_to_notify', []))
        for device_token in user_devices:
            PushClient().publish(
                PushMessage(
                    body=message,
                    sound='default',
                    title=title,
                    to=device_token,
                )
            )
