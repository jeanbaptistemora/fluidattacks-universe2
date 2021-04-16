# pylint:disable=cyclic-import,too-many-lines
"""Domain functions for projects."""

import logging
from typing import (
    Any,
    cast,
    Dict,
    List,
    Union,
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
    validations,
)
from notifications import domain as notifications_domain
from organizations import domain as orgs_domain
from resources import domain as resources_domain


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def edit(
    *,
    context: Any,
    comments: str,
    group_name: str,
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
    reason: str,
    requester_email: str,
    subscription: str,
) -> bool:
    success: bool = False
    is_continuous_type: bool = subscription == 'continuous'

    validations.validate_fields([comments])
    validations.validate_string_length_between(comments, 0, 250)
    groups_domain.validate_group_services_config(
        is_continuous_type,
        has_drills,
        has_forces,
        has_integrates)

    item = await project_dal.get_attributes(
        project_name=group_name,
        attributes=[
            'historic_configuration',
            'project_name'
        ]
    )
    item.setdefault('historic_configuration', [])

    if item.get('project_name'):
        success = await project_dal.update(
            data={
                'historic_configuration': cast(
                    List[Dict[str, Union[bool, str]]],
                    item['historic_configuration']
                ) + [{
                    'comments': comments,
                    'date': datetime_utils.get_as_str(
                        datetime_utils.get_now()
                    ),
                    'has_drills': has_drills,
                    'has_forces': has_forces,
                    'reason': reason,
                    'requester': requester_email,
                    'type': subscription,
                }],
            },
            project_name=group_name,
        )

    if not has_integrates:
        group_loader = context.group_all
        group = await group_loader.load(group_name)
        org_id = group['organization']
        success = success and await orgs_domain.remove_group(
            context,
            organization_id=org_id,
            group_name=group_name,
            email=requester_email,
        )

    if success and has_integrates:
        await notifications_domain.edit_group(
            comments=comments,
            group_name=group_name,
            had_drills=(
                cast(
                    bool,
                    cast(
                        List[Dict[str, Union[bool, str]]],
                        item['historic_configuration']
                    )[-1]['has_drills']
                )
                if item['historic_configuration'] else False
            ),
            had_forces=(
                cast(
                    bool,
                    cast(
                        List[Dict[str, Union[bool, str]]],
                        item['historic_configuration']
                    )[-1]['has_forces']
                )
                if item['historic_configuration'] else False
            ),
            had_integrates=True,
            has_drills=has_drills,
            has_forces=has_forces,
            has_integrates=has_integrates,
            reason=reason,
            requester_email=requester_email,
            subscription=subscription,
        )
    elif success and not has_integrates:
        await notifications_domain.delete_group(
            deletion_date=datetime_utils.get_as_str(
                datetime_utils.get_now()
            ),
            group_name=group_name,
            requester_email=requester_email,
        )

    return success


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
