# pylint: disable=import-error

from backend.domain import alert as alert_domain


def resolve_alert(*_, project_name, organization):
    """Resolve alert query."""
    result = {
        'message': str(),
        'project': str(),
        'organization': str(),
        'status': int()
    }
    resp = alert_domain.get_company_alert(organization, project_name)
    if resp:
        result['message'] = resp[0]['message']
        result['project'] = resp[0]['project_name']
        result['organization'] = resp[0]['company_name']
        result['status'] = resp[0]['status_act']
    return result
