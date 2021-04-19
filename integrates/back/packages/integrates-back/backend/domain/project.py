# pylint:disable=cyclic-import,too-many-lines
"""Domain functions for projects."""

import logging
from typing import (
    Any,
    cast,
    Dict,
    List,
)

from back.settings import LOGGING
from backend import authz
from backend.dal import project as project_dal
from backend.exceptions import AlreadyPendingDeletion
from backend.typing import Project as ProjectType
from groups import domain as groups_domain
from newutils import datetime as datetime_utils

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def delete_project(
    context: Any,
    project_name: str,
    user_email: str
) -> bool:
    response = False
    data = await project_dal.get_attributes(
        project_name,
        ['project_status', 'historic_deletion']
    )
    historic_deletion = cast(
        List[Dict[str, str]],
        data.get('historic_deletion', [])
    )
    if data.get('project_status') != 'DELETED':
        all_resources_removed = await groups_domain.remove_resources(
            context,
            project_name
        )
        today = datetime_utils.get_now()
        new_state = {
            'date': datetime_utils.get_as_str(today),
            'deletion_date': datetime_utils.get_as_str(today),
            'user': user_email.lower(),
        }
        historic_deletion.append(new_state)
        new_data: ProjectType = {
            'historic_deletion': historic_deletion,
            'project_status': 'DELETED'
        }
        response = all(
            [
                all_resources_removed,
                await project_dal.update(project_name, new_data)
            ]
        )
    else:
        raise AlreadyPendingDeletion()

    if response:
        await authz.revoke_cached_group_service_attributes_policies(
            project_name
        )

    return response
