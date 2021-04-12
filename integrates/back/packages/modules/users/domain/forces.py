# Standard libraries
import logging
import logging.config
import re

# Third-party libraries
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from back.settings import LOGGING
from backend.domain import project as group_domain
from groups import domain as groups_domain
from users.domain.group import complete_register_for_group_invitation


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def create_forces_user(
    info: GraphQLResolveInfo,
    group_name: str
) -> bool:
    user_email = format_forces_user_email(group_name)
    success = await groups_domain.invite_to_group(
        email=user_email,
        responsibility='Forces service user',
        role='service_forces',
        phone_number='',
        group_name=group_name
    )

    # Give permissions directly, no confirmation required
    group_access = await group_domain.get_user_access(user_email, group_name)
    success = (
        success and
        await complete_register_for_group_invitation(group_access)
    )

    if not success:
        LOGGER.error(
            'Couldn\'t grant access to project',
            extra={
                'extra': info.context,
                'username': group_name
            },
        )
    return success


def format_forces_user_email(project_name: str) -> str:
    return f'forces.{project_name}@fluidattacks.com'


def is_forces_user(email: str) -> bool:
    """Ensure that is an forces user."""
    pattern = r'forces.(?P<group>\w+)@fluidattacks.com'
    return bool(re.match(pattern, email))
