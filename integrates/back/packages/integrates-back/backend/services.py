""" Integrates services definition """

from typing import (
    cast,
    Dict,
)

from backend import (
    authz,
    util,
)
from events import domain as events_domain
from findings import domain as findings_domain
from users import domain as users_domain


async def has_access_to_project(email: str, group: str) -> bool:
    """ Verify if the user has access to a project. """
    return bool(await authz.get_group_level_role(email, group.lower()))


async def has_access_to_finding(email: str, finding_id: str) -> bool:
    """ Verify if the user has access to a finding submission. """
    finding = await findings_domain.get_finding(finding_id)
    group = cast(str, finding.get('projectName', ''))
    return await has_access_to_project(email, group)


async def has_access_to_event(email: str, event_id: str) -> bool:
    """ Verify if the user has access to a event submission. """
    event = await events_domain.get_event(event_id)
    group = cast(str, event.get('project_name', ''))
    return await has_access_to_project(email, group)


async def has_valid_access_token(
        email: str, context: Dict[str, str], jti: str) -> bool:
    """ Verify if has active access token and match. """
    access_token = cast(
        Dict[str, str],
        await users_domain.get_data(email, 'access_token')
    )
    resp = False
    if context and access_token:
        resp = util.verificate_hash_token(access_token, jti)
    else:
        # authorization header not present or user without access_token
        pass
    return resp
