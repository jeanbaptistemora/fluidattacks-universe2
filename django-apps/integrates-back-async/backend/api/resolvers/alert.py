from ariadne import convert_kwargs_to_snake_case
from asgiref.sync import sync_to_async

from backend.decorators import (
    enforce_group_level_auth_async, require_login,
    require_integrates,
    require_project_access, get_entity_cache_async
)
from backend.domain import alert as alert_domain
from backend.typing import (
    Alert as AlertType
)


@get_entity_cache_async
@sync_to_async
def _get_alert_fields(project_name: str, organization: str) -> AlertType:
    """Resolve alert query."""
    result: AlertType = dict(
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
@enforce_group_level_auth_async
@require_integrates
@require_project_access
async def resolve_alert(*_, project_name: str, organization: str) -> AlertType:
    """Resolve alert query."""
    return await _get_alert_fields(project_name, organization)
