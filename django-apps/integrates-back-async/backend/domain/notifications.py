# Local imports
from backend.dal import (
    notifications as notifications_dal,
)


def new_group(
    *,
    description: str,
    group_name: str,
    has_drills: bool,
    has_forces: bool,
    requester_email: str,
    subscription: str,
) -> bool:
    translations: dict = {
        'continuous': 'Continuous Hacking',
        'oneshot': 'One-Shot Hacking',
        True: 'Active',
        False: 'Inactive',
    }

    return notifications_dal.create_ticket(
        subject=f'[Integrates] Group created: {group_name}',
        description=f"""
            You are receiving this email because you have created a group
            through Integrates by Fluid Attacks.

            Here are the details of the group:
            - Name: {group_name}
            - Description: {description}
            - Type: {translations.get(subscription, subscription)}
            - Drills: {translations[has_drills]}
            - Forces: {translations[has_forces]}

            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=requester_email,
    )
