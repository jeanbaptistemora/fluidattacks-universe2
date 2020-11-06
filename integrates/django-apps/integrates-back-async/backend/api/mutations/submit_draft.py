# Submit
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import finding as finding_domain
from backend.typing import SimplePayload
from backend.utils import findings as finding_utils


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str
) -> SimplePayload:
    user_info = await util.get_jwt_content(info.context)
    analyst_email = user_info['user_email']
    success = await finding_domain.submit_draft(finding_id, analyst_email)

    if success:
        util.queue_cache_invalidation(finding_id)
        finding_loader = info.context.loaders['finding']
        finding = await finding_loader.load(finding_id)
        finding_domain.send_finding_mail(
            finding_utils.send_new_draft_mail,
            finding_id,
            str(finding.get('title', '')),
            str(finding.get('project_name', '')),
            analyst_email,
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Submitted draft {finding_id} successfully'
        )
    return SimplePayload(success=success)
