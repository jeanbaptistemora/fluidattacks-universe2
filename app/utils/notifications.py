from exponent_server_sdk import PushClient, PushMessage
from i18n import t

from app.dal import integrates_dal


def notify_mobile(recipients, title, message):
    message += t('notifications.details')
    for user_email in recipients:
        user_devices = integrates_dal.get_table_attributes_dynamo(
            'FI_users',
            {'email': user_email},
            ['devices_to_notify']).get('devices_to_notify', [])
        for device_token in user_devices:
            PushClient().publish(
                PushMessage(
                    body=message,
                    sound='default',
                    title=title,
                    to=device_token,
                )
            )
