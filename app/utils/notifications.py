from exponent_server_sdk import PushClient, PushMessage
from i18n import t

from app.dao import integrates_dao


def notify_mobile(recipients, title, message):
    for user_email in recipients:
        user_devices = integrates_dao.get_table_attributes_dynamo(
            'FI_users',
            {'email': user_email},
            ['devices_to_notify']).get('devices_to_notify', [])
        for device_token in user_devices:
            message += t('notifications.details')
            PushClient().publish(
                PushMessage(
                    body=message,
                    sound='default',
                    title=title,
                    to=device_token,
                )
            )
