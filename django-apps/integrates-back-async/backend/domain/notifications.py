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
) -> bool:
    return notifications_dal.create_ticket(
        subject=f'[Integrates] Group created: {group_name}',
        description=f"""
            You are receiving this email because you have created a group
            through integrates by Fluid Attacks.

            Here are the details of the group:
            - Name: {group_name}
            - Description: {description}
            - Has Drills: {has_drills}
            - Has Forces: {has_forces}

            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=requester_email,
    )
