# pylint:disable=too-many-lines
import logging
import sys
from time import time
from typing import Any, Union, cast

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
from backend.exceptions import PermissionDenied
from backend.typing import (
    SimplePayload as SimplePayloadType,
    SimpleFindingPayload as SimpleFindingPayloadType,
    ApproveDraftPayload as ApproveDraftPayloadType,
    AddConsultPayload as AddConsultPayloadType,
)
from backend.utils import (
    datetime as datetime_utils,
    findings as finding_utils,
)
from backend import util
from backend_new.settings import LOGGING

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
    return cast(
        Union[
            SimpleFindingPayloadType,
            SimplePayloadType,
            AddConsultPayloadType,
            ApproveDraftPayloadType
        ],
        resolver_func(obj, info, **parameters)
    )


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def _do_remove_evidence(
        _: Any,
        info: GraphQLResolveInfo,
        evidence_id: str,
        finding_id: str) -> SimpleFindingPayloadType:
    """Resolve remove_evidence mutation."""
    success = await finding_domain.remove_evidence(evidence_id, finding_id)

    if success:
        util.queue_cache_invalidation(
            f'evidence*{finding_id}',
            f'exploit*{finding_id}',
            f'records*{finding_id}'
        )
        util.cloudwatch_log(
            info.context,
            ('Security: Removed evidence '
             f'in finding {finding_id}')  # pragma: no cover
        )
    finding = await info.context.loaders['finding'].load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def _do_add_finding_consult(
        _: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> AddConsultPayloadType:
    success = False
    param_type = parameters.get('type', '').lower()
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    finding_id = str(parameters.get('finding_id'))
    finding_loader = info.context.loaders['finding']
    finding = await finding_loader.load(finding_id)
    group = finding.get('project_name')
    content = parameters['content']

    user_email = user_data['user_email']
    comment_id = int(round(time() * 1000))
    current_time = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
    comment_data = {
        'user_id': comment_id,
        'comment_type': param_type if param_type != 'consult' else 'comment',
        'content': content,
        'fullname': ' '.join(
            [user_data['first_name'], user_data['last_name']]
        ),
        'parent': parameters.get('parent'),
        'created': current_time,
        'modified': current_time,
    }
    try:
        success = await finding_domain.add_comment(
            info,
            user_email,
            comment_data,
            finding_id,
            group
        )
    except PermissionDenied:
        util.cloudwatch_log(
            info.context,
            'Security: Unauthorized role attempted to add observation'
        )

    if success:
        util.queue_cache_invalidation(
            f'{param_type}*{finding_id}',
            f'comment*{finding_id}'
        )
        if content.strip() not in {'#external', '#internal'}:
            finding_domain.send_comment_mail(
                user_email,
                comment_data,
                finding
            )

        util.cloudwatch_log(
            info.context,
            ('Security: Added comment in '
             f'finding {finding_id} successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to add '
             f'comment in finding {finding_id}')  # pragma: no cover
        )
    ret = AddConsultPayloadType(success=success, comment_id=str(comment_id))
    return ret


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
