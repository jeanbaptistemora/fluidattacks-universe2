# pylint:disable=cyclic-import,too-many-lines
"""Domain functions for projects."""

import logging
from typing import (
    Any,
    cast,
    Dict,
    List,
)

from aioextensions import collect

from back.settings import LOGGING
from backend import authz
from backend.dal import project as project_dal
from backend.exceptions import AlreadyPendingDeletion
from backend.typing import Project as ProjectType
from events import domain as events_domain
from findings import domain as findings_domain
from group_access import domain as group_access_domain
from groups import domain as groups_domain
from newutils import (
    datetime as datetime_utils,
    user as user_utils,
)
from organizations import domain as orgs_domain
from resources import domain as resources_domain


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def remove_resources(context: Any, project_name: str) -> bool:
    are_users_removed = await remove_all_users_access(context, project_name)
    group_findings = await findings_domain.list_findings(
        context,
        [project_name],
        include_deleted=True
    )
    group_drafts = await findings_domain.list_drafts(
        [project_name], include_deleted=True
    )
    findings_and_drafts = (
        group_findings[0] + group_drafts[0]
    )
    are_findings_masked = all(await collect(
        findings_domain.mask_finding(context, finding_id)
        for finding_id in findings_and_drafts
    ))
    events = await events_domain.list_group_events(project_name)
    are_events_masked = all(await collect(
        events_domain.mask(event_id)
        for event_id in events
    ))
    is_group_masked = await groups_domain.mask(project_name)
    are_resources_masked = all(
        list(
            cast(List[bool], await resources_domain.mask(project_name))
        )
    )

    response = all(
        [
            are_findings_masked,
            are_users_removed,
            is_group_masked,
            are_events_masked,
            are_resources_masked
        ]
    )

    return response


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
        all_resources_removed = await remove_resources(context, project_name)
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


async def remove_all_users_access(context: Any, project: str) -> bool:
    """Remove user access to project."""
    user_active, user_suspended = await collect([
        group_access_domain.get_group_users(project, True),
        group_access_domain.get_group_users(project, False)
    ])
    all_users = user_active + user_suspended
    are_users_removed = all(await collect([
        remove_user_access(context, project, user)
        for user in all_users
    ]))

    return are_users_removed


async def remove_user_access(
    context: Any,
    group_name: str,
    email: str,
    check_org_access: bool = True
) -> bool:
    """Remove user access to project."""
    success: bool = all(
        await collect([
            authz.revoke_group_level_role(email, group_name),
            group_access_domain.remove_access(email, group_name)
        ])
    )
    if success and check_org_access:
        group_loader = context.group
        group = await group_loader.load(group_name)
        org_id = group['organization']
        has_org_access = await orgs_domain.has_user_access(org_id, email)
        has_groups_in_org = bool(
            await groups_domain.get_groups_by_user(
                email,
                organization_id=org_id
            )
        )
        if has_org_access and not has_groups_in_org:
            success = success and await orgs_domain.remove_user(
                context,
                org_id,
                email
            )

        has_groups = bool(
            await groups_domain.get_groups_by_user(email)
        )
        if not has_groups:
            success = success and await user_utils.remove_stakeholder(email)

    return success
