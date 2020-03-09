# pylint: disable=import-error

from ariadne import convert_kwargs_to_snake_case
from backend.domain import alert as alert_domain
from backend import util


@convert_kwargs_to_snake_case
def resolve_alert(*_, project_name, organization):
    """Resolve alert query."""
    result = dict()
    resp = alert_domain.get_company_alert(organization, project_name)
    if resp:
        result['message'] = resp[0]['message']
        result['project'] = resp[0]['project_name']
        result['organization'] = resp[0]['company_name']
        result['status'] = resp[0]['status_act']
    return result


@convert_kwargs_to_snake_case
def resolve_set_alert(_, info, company, message, project_name):
    success = alert_domain.set_company_alert(
        company, message, project_name)
    if success:
        util.cloudwatch_log(
            info.context, f'Security: Set alert of {company}')
    return dict(success=success)
