""" FluidIntegrates services definition """

from typing import Dict, cast
from backend.domain import (
    event as event_domain,
    finding as finding_domain,
    user as user_domain
)

from backend import authz, util


async def has_access_to_project(email: str, group: str) -> bool:
    """ Verify if the user has access to a project. """
    return bool(await authz.get_group_level_role(email, group.lower()))


async def has_access_to_finding(email: str, finding_id: str) -> bool:
    """ Verify if the user has access to a finding submission. """
    finding = await finding_domain.get_finding(finding_id)
    group = cast(str, finding.get('projectName', ''))
    return await has_access_to_project(email, group)


async def has_access_to_event(email: str, event_id: str) -> bool:
    """ Verify if the user has access to a event submission. """
    event = await event_domain.get_event(event_id)
    group = cast(str, event.get('project_name', ''))
    return await has_access_to_project(email, group)


async def has_valid_access_token(
        email: str, context: Dict[str, str], jti: str) -> bool:
    """ Verify if has active access token and match. """
    access_token = cast(
        Dict[str, str],
        await user_domain.get_data(email, 'access_token')
    )
    resp = False
    if context and access_token:
        resp = util.verificate_hash_token(access_token, jti)
    else:
        # authorization header not present or user without access_token
        pass
    return resp
