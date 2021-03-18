# Standard libraries
from typing import Dict

# Local libraries
from backend import authz
from backend.domain import project as group_domain
from backend.typing import Invitation as InvitationType
from newutils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
    validate_fluidattacks_staff_on_group,
    validate_phone_field
)


async def update_invited_stakeholder(
    updated_data: Dict[str, str],
    invitation: InvitationType,
    group_name: str
) -> bool:
    success = False
    email = updated_data['email']
    responsibility = updated_data['responsibility']
    phone_number = updated_data['phone_number']
    role = updated_data['role']
    new_invitation = invitation.copy()
    if (
        validate_field_length(responsibility, 50)
        and validate_alphanumeric_field(responsibility)
        and validate_phone_field(phone_number)
        and validate_email_address(email)
        and await validate_fluidattacks_staff_on_group(group_name, email, role)

    ):
        new_invitation['phone_number'] = phone_number
        new_invitation['responsibility'] = responsibility
        new_invitation['role'] = role

        success = await group_domain.update_access(
            email,
            group_name,
            {
                'invitation': new_invitation,

            }
        )

    return success


def is_fluid_staff(email: str) -> bool:
    return email.endswith('@fluidattacks.com')


async def is_manager(email: str, group_name: str) -> bool:
    role: str = await authz.get_group_level_role(email, group_name)

    return role == 'group_manager'
