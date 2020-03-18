# pylint: disable=import-error

from backend.decorators import (
    get_cached, enforce_authz_async, require_login,
    require_project_access
)
from backend.domain import alert as alert_domain
from backend import util

from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_project_access
@get_cached
def resolve_alert(*_, project_name, organization):
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
