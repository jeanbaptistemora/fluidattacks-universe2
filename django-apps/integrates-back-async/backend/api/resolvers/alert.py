# pylint: disable=import-error

from ariadne import convert_kwargs_to_snake_case
from backend.domain import alert as alert_domain


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
