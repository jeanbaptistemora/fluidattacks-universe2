# pylint: disable=import-error

import asyncio

from typing import Dict
from asgiref.sync import sync_to_async
from backend.decorators import (
    enforce_group_level_auth_async, require_login,
    require_project_access
)
from backend.domain import alert as alert_domain
from backend.typing import Alert as AlertType
from backend import util

from ariadne import convert_kwargs_to_snake_case


@sync_to_async
def _get_alert_fields(project_name: str, organization: str) -> AlertType:
    """Resolve alert query."""
    result = dict(
        message=str(),
        project=str(),
        organization=str(),
        status=int())
    resp = alert_domain.get_company_alert(organization, project_name)
    if resp:
        result['message'] = resp[0]['message']
        result['project'] = resp[0]['project_name']
        result['organization'] = resp[0]['company_name']
        result['status'] = resp[0]['status_act']
    return result


async def _resolve_fields(project_name: str, organization: str) -> AlertType:
    """Async resolve fields."""
    result = dict()
    future = asyncio.ensure_future(
        _get_alert_fields(project_name, organization)
    )
    tasks_result = await asyncio.gather(future)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_alert(*_, project_name: str, organization: str) -> AlertType:
    """Resolve alert query."""
    return util.run_async(_resolve_fields, project_name, organization)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
def resolve_set_alert(_, info, company: str, message: str,
                      project_name: str) -> Dict[str, bool]:
    """Resolve set_alert mutation."""
    success = alert_domain.set_company_alert(
        company, message, project_name)
    if success:
        util.cloudwatch_log(
            info.context, f'Security: Set alert of {company}')
    return dict(success=success)
