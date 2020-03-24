# pylint: disable=import-error

from backend.decorators import (
    enforce_authz_async, require_login,
    require_finding_access
)
from backend.domain import finding as finding_domain
from backend import util

from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_finding_access
def resolve_remove_evidence(_, info, evidence_id, finding_id):
    """Resolve remove_evidence mutation."""
    success = finding_domain.remove_evidence(evidence_id, finding_id)

    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: Removed evidence in finding {finding_id}')
        util.invalidate_cache(finding_id)
    return dict(success=success)
