# pylint: disable=import-error

import asyncio

from backend.decorators import (
    get_cached, enforce_authz_async, require_login,
    require_project_access
)
from backend.domain import alert as alert_domain
from backend import util

from ariadne import convert_kwargs_to_snake_case


async def _get_alert_fields(project_name, organization):
    """Resolve alert query."""
    result = dict(
        message=str(),
        project=str(),
        organization=str(),
        status=int())
    resp = alert_domain.get_company_alert(organization, project_name)
    await asyncio.sleep(0)
    if resp:
        result['message'] = resp[0]['message']
        result['project'] = resp[0]['project_name']
        result['organization'] = resp[0]['company_name']
        result['status'] = resp[0]['status_act']
    return result


async def _resolve_fields(project_name, organization):
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
@enforce_authz_async
@require_project_access
@get_cached
def resolve_alert(*_, project_name, organization):
    """Resolve alert query."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        _resolve_fields(project_name, organization)
    )
    loop.close()
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
def resolve_set_alert(_, info, company, message, project_name):
    """Resolve set_alert mutation."""
    success = alert_domain.set_company_alert(
        company, message, project_name)
    if success:
        util.cloudwatch_log(
            info.context, f'Security: Set alert of {company}')
    return dict(success=success)
