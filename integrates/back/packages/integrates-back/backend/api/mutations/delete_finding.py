# Standard
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
    finding_id: str,
    justification: str
) -> SimplePayload:
    finding_loader = info.context.loaders['finding']
    finding_data = await finding_loader.load(finding_id)
    group_name = finding_data['project_name']

    success = await finding_domain.delete_finding(
        finding_id, justification, info.context
    )
    if success:
        util.queue_cache_invalidation(
            f'finding*{group_name}',
            f'severity*{group_name}',
            f'vuln*{group_name}',
            finding_id
        )
        justification_dict = {
            'DUPLICATED': 'It is duplicated',
            'FALSE_POSITIVE': 'It is a false positive',
            'NOT_REQUIRED': 'Finding not required',
        }
        finding_domain.send_finding_mail(
            finding_utils.send_finding_delete_mail,
            finding_id,
            str(finding_data.get('finding', '')),
            group_name,
            str(finding_data.get('analyst', '')),
            justification_dict[justification]
        )
        util.forces_trigger_deployment(group_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Deleted finding: {finding_id} successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to delete finding: {finding_id}'
        )
    return SimplePayload(success=success)
