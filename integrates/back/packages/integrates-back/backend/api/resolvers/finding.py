# pylint:disable=too-many-lines
import logging
import sys
from typing import Any, Union

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login, require_finding_access
)
from backend.domain import (
    finding as finding_domain,
)
from backend.typing import (
    SimplePayload as SimplePayloadType,
    SimpleFindingPayload as SimpleFindingPayloadType,
    ApproveDraftPayload as ApproveDraftPayloadType,
    AddConsultPayload as AddConsultPayloadType,
)
from backend.utils import (
    findings as finding_utils
)
from backend import util
from back.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case  # type: ignore
def resolve_finding_mutation(
        obj: Any,
        info: GraphQLResolveInfo,
        **parameters: Any
) -> Union[
    SimpleFindingPayloadType,
    SimplePayloadType,
    AddConsultPayloadType,
    ApproveDraftPayloadType
]:
    """Resolve findings mutation."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return resolver_func(obj, info, **parameters)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def _do_update_description(
        _: Any,
        info: GraphQLResolveInfo,
        finding_id: str,
        **parameters: Any) -> SimpleFindingPayloadType:
    """Perform update_description mutation."""
    success = await finding_domain.update_description(
        finding_id, parameters
    )
    if success:
        attrs_to_clean = {attribute: finding_id for attribute in parameters}
        to_clean = util.format_cache_keys_pattern(attrs_to_clean)
        util.queue_cache_invalidation(*to_clean)
        util.cloudwatch_log(
            info.context,
            ('Security: Updated description in '
             'finding {finding_id} successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to update '
             f'description in finding {finding_id}')  # pragma: no cover
        )
    finding = await info.context.loaders['finding'].load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def _do_reject_draft(
        _: Any,
        info: GraphQLResolveInfo,
        finding_id: str) -> SimplePayloadType:
    """Resolve reject_draft mutation."""
    user_info = await util.get_jwt_content(info.context)
    reviewer_email = user_info['user_email']
    success = await finding_domain.reject_draft(finding_id, reviewer_email)
    if success:
        util.queue_cache_invalidation(finding_id)
        finding_loader = info.context.loaders['finding']
        finding = await finding_loader.load(finding_id)
        finding_domain.send_finding_mail(
            finding_utils.send_draft_reject_mail,
            finding_id,
            str(finding.get('title', '')),
            str(finding.get('project_name', '')),
            str(finding.get('analyst', '')),
            reviewer_email
        )
        util.cloudwatch_log(
            info.context,
            (f'Security: Draft {finding_id}'
             'rejected successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to reject '
             f'draft {finding_id}')  # pragma: no cover
        )
    return SimplePayloadType(success=success)
