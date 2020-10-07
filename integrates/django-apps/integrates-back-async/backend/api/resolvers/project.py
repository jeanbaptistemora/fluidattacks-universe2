# Standard library  # pylint:disable=cyclic-import
# pylint:disable=too-many-lines
import asyncio
import logging
import sys
import time
from typing import Dict, List, Set, Any, cast, Union

# Third party libraries
from aioextensions import (
    collect,
)
import simplejson as json
from ariadne import (
    convert_camel_case_to_snake,
    convert_kwargs_to_snake_case,
)
from graphql import GraphQLError
from graphql.language.ast import (
    FieldNode,
    SelectionSetNode,
    ObjectFieldNode
)
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import authz
from backend.api.resolvers import (
    finding as finding_loader,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    get_entity_cache_async,
    require_login,
    turn_args_into_kwargs,
    require_integrates,
    enforce_user_level_auth_async
)
from backend.domain import (
    project as project_domain,
    user as user_domain,
)
from backend.typing import (
    Event as EventType,
    Finding as FindingType,
    Project as ProjectType,
    AddConsultPayload as AddConsultPayloadType,
    SimplePayload as SimplePayloadType,
    SimpleProjectPayload as SimpleProjectPayloadType,
)
from backend import util
from backend.utils import (
    aio,
    datetime as datetime_utils,
)
from backend.api.resolvers.user import _create_new_user
from fluidintegrates.settings import LOGGING


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_name(
        _: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> str:
    """Get name."""
    return project_name


@get_entity_cache_async
async def _get_has_drills(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> bool:
    """Get has_drills."""
    project_attrs = await info.context.loaders['project'].load(project_name)

    return cast(
        bool,
        project_attrs['attrs']['historic_configuration'][-1]['has_drills']
    )


@get_entity_cache_async
async def _get_has_forces(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> bool:
    """Get has_forces."""
    project_attrs = await info.context.loaders['project'].load(project_name)

    return cast(
        bool,
        project_attrs['attrs']['historic_configuration'][-1]['has_forces']
    )


@get_entity_cache_async
async def _get_has_integrates(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> bool:
    """Get has_forces."""
    project_attrs = await info.context.loaders['project'].load(project_name)

    return cast(
        bool,
        project_attrs['attrs']['project_status'] == 'ACTIVE'
    )


@require_integrates
async def _get_findings(
    info: GraphQLResolveInfo,
    project_name: str,
    requested_fields: List[FieldNode],
    filters: Union[None, List[Union[None, ObjectFieldNode]]] = None
) -> List[Dict[str, FindingType]]:
    """Resolve findings attribute."""

    req_fields: List[Union[FieldNode, ObjectFieldNode]] = []
    selection_set = SelectionSetNode()
    selection_set.selections = requested_fields
    req_fields.extend(util.get_requested_fields('findings', selection_set))
    if filters:
        req_fields.extend(filters)
    selection_set.selections = req_fields
    util.cloudwatch_log(
        info.context,
        f'Security: Access to {project_name} findings'  # pragma: no cover
    )
    project_findings = await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    findings = await info.context.loaders['finding'].load_many(
        project_findings
    )
    findings = [
        finding for finding in findings
        if 'current_state' in finding and finding['current_state'] != 'DELETED'
    ]
    findings = await asyncio.gather(*[
        asyncio.create_task(
            finding_loader.resolve(
                info,
                finding['id'],
                as_field=True,
                selection_set=selection_set
            )
        )
        for finding in findings
    ])
    return cast(
        List[Dict[str, FindingType]],
        (
            await util.get_filtered_elements(findings, filters)
            if filters else findings
        )
    )


@require_integrates
@get_entity_cache_async
async def _get_open_vulnerabilities(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Get open_vulnerabilities."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    open_vulnerabilities = project_attrs.get('open_vulnerabilities', 0)
    return cast(int, open_vulnerabilities)


@require_integrates
@get_entity_cache_async
async def _get_open_findings(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Get open_findings."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    open_findings = project_attrs.get('open_findings', 0)
    return cast(int, open_findings)


@require_integrates
@get_entity_cache_async
async def _get_closed_vulnerabilities(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Get closed_vulnerabilities."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    closed_vulnerabilities = project_attrs.get('closed_vulnerabilities', 0)
    return cast(int, closed_vulnerabilities)


@require_integrates
@get_entity_cache_async
async def _get_last_closing_vuln(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Get last_closing_vuln."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    last_closing_vuln = project_attrs.get('last_closing_date', 0)
    return cast(int, last_closing_vuln)


@require_integrates
@get_entity_cache_async
async def _get_last_closing_vuln_finding(
        info: GraphQLResolveInfo,
        project_name: str,
        requested_fields: List[FieldNode]) -> Dict[str, FindingType]:
    """Resolve finding attribute."""
    req_fields: List[Union[FieldNode, ObjectFieldNode]] = []
    selection_set = SelectionSetNode()
    selection_set.selections = requested_fields
    req_fields.extend(
        util.get_requested_fields('lastClosingVulnFinding', selection_set)
    )
    selection_set.selections = req_fields
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    last_closing_vuln_finding = project_attrs.get(
        'last_closing_vuln_finding', ''
    )
    finding = await finding_loader.resolve(
        info,
        last_closing_vuln_finding,
        as_field=True,
        selection_set=selection_set
    )

    return cast(Dict[str, FindingType], await aio.materialize(finding))


@require_integrates
@get_entity_cache_async
async def _get_max_severity(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> float:
    """Get max_severity."""
    project_findings = await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    findings = await info.context.loaders['finding'].load_many(
        project_findings
    )

    max_severity = max([
        finding['severity_score']
        for finding in findings
        if ('current_state' in finding and
            finding['current_state'] != 'DELETED')
    ]) if findings else 0
    return cast(float, max_severity)


@require_integrates
@get_entity_cache_async
async def _get_max_severity_finding(
        info: GraphQLResolveInfo,
        project_name: str,
        requested_fields: List[FieldNode]) -> Dict[str, FindingType]:
    """Resolve finding attribute."""
    req_fields: List[Union[FieldNode, ObjectFieldNode]] = []
    selection_set = SelectionSetNode()
    selection_set.selections = requested_fields
    req_fields.extend(
        util.get_requested_fields('maxSeverityFinding', selection_set))
    selection_set.selections = req_fields
    project_findings = await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    findings = await info.context.loaders['finding'].load_many(
        project_findings
    )
    _, max_severity_finding = max([
        (finding['severity_score'], finding['id'])
        for finding in findings
        if 'current_state' in finding and
        finding['current_state'] != 'DELETED'
    ]) if findings else (0, '')
    finding = await finding_loader.resolve(
        info, max_severity_finding,
        as_field=True, selection_set=selection_set)

    return cast(Dict[str, FindingType], await aio.materialize(finding))


@require_integrates
@get_entity_cache_async
async def _get_max_open_severity(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Resolve maximum severity in open vulnerability attribute."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return cast(int, project_attrs.get('max_open_severity', 0))


@require_integrates
@get_entity_cache_async
async def _get_max_open_severity_finding(
        info: GraphQLResolveInfo,
        project_name: str,
        requested_fields: List[FieldNode]) -> Dict[str, FindingType]:
    """Resolve finding attribute."""
    req_fields: List[Union[FieldNode, ObjectFieldNode]] = []
    selection_set = SelectionSetNode()
    selection_set.selections = requested_fields
    req_fields.extend(
        util.get_requested_fields('maxOpenSeverityFinding', selection_set)
    )
    selection_set.selections = req_fields
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    max_open_severity_finding = project_attrs.get(
        'max_open_severity_finding', ''
    )
    finding = await finding_loader.resolve(
        info,
        max_open_severity_finding,
        as_field=True,
        selection_set=selection_set
    )

    return cast(Dict[str, FindingType], await aio.materialize(finding))


@require_integrates
@get_entity_cache_async
async def _get_mean_remediate(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Get mean_remediate."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return cast(int, project_attrs.get('mean_remediate', 0))


@require_integrates
@get_entity_cache_async
async def _get_mean_remediate_low_severity(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Get mean_remediate_low_severity."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return cast(int, project_attrs.get('mean_remediate_low_severity', 0))


@require_integrates
@get_entity_cache_async
async def _get_mean_remediate_medium_severity(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Get mean_remediate_medium_severity."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return cast(int, project_attrs.get('mean_remediate_medium_severity', 0))


@require_integrates
@get_entity_cache_async
async def _get_mean_remediate_high_severity(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Get mean_remediate_high_severity."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return cast(int, project_attrs.get('mean_remediate_high_severity', 0))


@require_integrates
@get_entity_cache_async
async def _get_mean_remediate_critical_severity(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Get mean_remediate_critical_severity."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return cast(int, project_attrs.get('mean_remediate_critical_severity', 0))


@require_integrates
@get_entity_cache_async
async def _get_total_findings(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> int:
    """Get total_findings."""
    project_findings = await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    findings = await info.context.loaders['finding'].load_many(
        project_findings
    )

    total_findings = sum(
        1 for finding in findings
        if ('current_state' in finding and
            finding['current_state'] != 'DELETED')
    )
    return total_findings


@require_integrates
@get_entity_cache_async
async def _get_total_treatment(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> str:
    """Get total_treatment."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    total_treatment_decimal = project_attrs.get('total_treatment', {})
    total_treatment = json.dumps(
        total_treatment_decimal, use_decimal=True
    )
    return total_treatment


@get_entity_cache_async
async def _get_subscription(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> str:
    """Get subscription."""
    project_attrs = await info.context.loaders['project'].load(project_name)

    return cast(
        str,
        project_attrs['attrs']['historic_configuration'][-1]['type']
    )


# Intentionally not @require_integrates
@get_entity_cache_async
async def _get_deletion_date(
        _: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> str:
    """Get deletion_date."""
    historic_deletion = await project_domain.get_historic_deletion(
        project_name
    )
    deletion_date = (
        historic_deletion[-1].get('deletion_date', '')
        if historic_deletion else ''
    )
    return deletion_date


# Intentionally not @require_integrates
@get_entity_cache_async
async def _get_user_deletion(
        _: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> str:
    """Get user_deletion."""
    user_deletion = ''
    historic_deletion = await project_domain.get_historic_deletion(
        project_name
    )
    if historic_deletion and historic_deletion[-1].get('deletion_date'):
        user_deletion = historic_deletion[-1].get('user', '')
    return user_deletion


@require_integrates
@get_entity_cache_async
async def _get_tags(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> Set[str]:
    """Get tags."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attrs = project_attrs['attrs']
    return cast(Set[str], project_attrs.get('tag', []))


# Intentionally not @require_integrates
@get_entity_cache_async
async def _get_description(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> str:
    """Get description."""
    project_attrs = await info.context.loaders['project'].load(project_name)
    project_attr = project_attrs['attrs']
    return cast(str, project_attr.get('description', ''))


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def _get_drafts(
        info: GraphQLResolveInfo,
        project_name: str,
        requested_fields: List[FieldNode],
        **__: Any) -> List[Dict[str, FindingType]]:
    """Get drafts."""
    util.cloudwatch_log(
        info.context,
        f'Security: Access to {project_name} drafts')  # pragma: no cover
    selection_set = SelectionSetNode()
    selection_set.selections = requested_fields
    selection_set.selections = util.get_requested_fields(
        'drafts', selection_set
    )

    project_drafts = await info.context.loaders['project'].load(project_name)
    project_drafts = project_drafts['drafts']
    findings = await info.context.loaders['finding'].load_many(project_drafts)

    drafts = [
        draft for draft in findings
        if ('current_state' in draft and
            draft['current_state'] != 'DELETED')
    ]

    return await collect(
        finding_loader.resolve(
            info,
            draft['id'],
            as_field=True,
            selection_set=selection_set
        )
        for draft in drafts
    )


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def _get_events(
        info: GraphQLResolveInfo,
        project_name: str,
        **__: Any) -> List[EventType]:
    """Get events."""
    util.cloudwatch_log(
        info.context,
        f'Security: Access to {project_name} events')  # pragma: no cover
    event_ids = await project_domain.list_events(project_name)
    events = await info.context.loaders['event'].load_many(event_ids)
    return cast(List[EventType], events)


def _get_requested_fields(
        info: GraphQLResolveInfo,
        as_field: bool,
        as_list: bool) -> List[FieldNode]:
    if as_field and as_list:
        to_extend = util.get_requested_fields(
            'projects',
            info.field_nodes[0].selection_set
        )
    elif as_field:
        to_extend = util.get_requested_fields(
            'project',
            info.field_nodes[0].selection_set
        )
    else:
        to_extend = info.field_nodes[0].selection_set.selections
    return to_extend


async def resolve(
        info: GraphQLResolveInfo,
        project_name: str,
        as_field: bool = False,
        as_list: bool = True,
        selection_set: Union[SelectionSetNode, None] = None) -> ProjectType:
    """Async resolve fields."""
    project_name = project_name.lower()
    result: ProjectType = dict()
    req_fields: List[Union[FieldNode, ObjectFieldNode]] = []

    req_fields.extend(_get_requested_fields(info, as_field, as_list))

    if selection_set:
        req_fields.extend(selection_set.selections)

    for requested_field in req_fields:
        if util.is_skippable(info, requested_field):
            continue
        params = {
            'project_name': project_name,
            'requested_fields': req_fields
        }
        field_params = util.get_field_parameters(
            requested_field, info.variable_values
        )

        if field_params:
            params.update(field_params)
        requested_field = convert_camel_case_to_snake(
            requested_field.name.value
        )
        migrated = {
            'analytics',
            'bill',
            'consulting',
            'organization',
            'service_attributes',
            'stakeholders',
            'user_role'
        }
        if requested_field.startswith('_') or requested_field in migrated:
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = resolver_func(info, **params)
    collected = dict(zip(result, await collect(result.values())))
    return {'name': project_name, **collected}


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve_project(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str) -> ProjectType:
    """Resolve project query."""
    project = await info.context.loaders['project'].load(project_name.lower())
    if not project['attrs'] or project['attrs'].get('deletion_date'):
        raise GraphQLError('Access denied')
    return await resolve(info, project_name)


@convert_kwargs_to_snake_case  # type: ignore
async def resolve_project_mutation(
        obj: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> Any:
    """Wrap project mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)


async def _create_forces_user(info: GraphQLResolveInfo,
                              group_name: str) -> bool:
    success = await _create_new_user(
        context=info.context,
        email=user_domain.format_forces_user_email(group_name),
        responsibility='Forces service user',
        role='service_forces',
        phone_number='',
        group=group_name)
    if not success:
        LOGGER.error(
            'Couldn\'t grant access to project',
            extra={
                'extra': info.context,
                'username': group_name
            },
        )
    return success


@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def _do_create_project(  # pylint: disable=too-many-arguments
        _: Any,
        info: GraphQLResolveInfo,
        description: str,
        organization: str,
        project_name: str,
        subscription: str = 'continuous',
        has_drills: bool = False,
        has_forces: bool = False) -> SimplePayloadType:
    """Resolve create_project mutation."""
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    user_role = await authz.get_user_level_role(user_email)

    success = await project_domain.create_project(
        user_email,
        user_role,
        project_name.lower(),
        organization,
        description,
        has_drills,
        has_forces,
        subscription
    )

    if success and has_forces:
        await _create_forces_user(info, project_name)
    if success:
        util.queue_cache_invalidation(user_email)
        util.cloudwatch_log(
            info.context,
            f'Security: Created project {project_name.lower()} successfully',
        )

    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
@turn_args_into_kwargs
async def _do_edit_group(  # pylint: disable=too-many-arguments
    _: Any,
    info: GraphQLResolveInfo,
    comments: str,
    group_name: str,
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
    reason: str,
    subscription: str
) -> SimplePayloadType:
    group_name = group_name.lower()
    user_info = await util.get_jwt_content(info.context)
    requester_email = user_info['user_email']

    success = await project_domain.edit(
        comments=comments,
        group_name=group_name,
        has_drills=has_drills,
        has_forces=has_forces,
        has_integrates=has_integrates,
        reason=reason,
        requester_email=requester_email,
        subscription=subscription,
    )
    if success and has_forces:
        await _create_forces_user(info, group_name)
    elif success and not has_forces and await user_domain.ensure_user_exists(
            user_domain.format_forces_user_email(group_name)):
        await project_domain.remove_user_access(
            group_name, user_domain.format_forces_user_email(group_name))
    if success:
        await util.invalidate_cache(group_name, requester_email)
        await authz.revoke_cached_group_service_attributes_policies(group_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Edited group {group_name} successfully',
        )

    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
# Intentionally not @require_integrates
async def _do_reject_remove_project(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str) -> SimplePayloadType:
    """Resolve reject_remove_project mutation."""
    user_info = await util.get_jwt_content(info.context)
    success = await project_domain.reject_deletion(
        project_name, user_info['user_email']
    )
    if success:
        project = project_name.lower()
        util.queue_cache_invalidation(project)
        util.cloudwatch_log(
            info.context,
            'Security: Reject project '
            f'{project} deletion successfully'  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_add_project_consult(
        _: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> AddConsultPayloadType:
    project_name = parameters.get('project_name', '').lower()
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    current_time = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
    comment_id = int(round(time.time() * 1000))
    comment_data = {
        'user_id': comment_id,
        'content': parameters.get('content'),
        'created': current_time,
        'fullname': str.join(
            ' ',
            [user_info['first_name'], user_info['last_name']]
        ),
        'modified': current_time,
        'parent': parameters.get('parent')
    }
    success = await project_domain.add_comment(
        project_name,
        user_email,
        comment_data
    )
    if success:
        util.queue_cache_invalidation(
            f'consulting*{project_name}',
            f'comment*{project_name}'
        )
        project_domain.send_comment_mail(
            user_email,
            comment_data,
            project_name
        )
        util.cloudwatch_log(
            info.context, 'Security: Added comment to '
            f'{project_name} project successfully'  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context, 'Security: Attempted to add '
            f'comment in {project_name} project'  # pragma: no cover
        )
    ret = AddConsultPayloadType(success=success, comment_id=str(comment_id))
    return ret


async def _update_tags(
        project_name: str,
        project_tags: ProjectType,
        tags: List[str]) -> bool:
    if not project_tags['tag']:
        project_tags = {'tag': set(tags)}
    else:
        cast(Set[str], project_tags.get('tag')).update(tags)
    tags_added = await project_domain.update(project_name, project_tags)
    if tags_added:
        success = True
    else:
        LOGGER.error('Couldn\'t add tags', extra={'extra': locals()})
        success = False
    return success


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_add_tags(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        tags: List[str]) -> SimpleProjectPayloadType:
    """Resolve add_tags mutation."""
    success = False
    project_name = project_name.lower()
    if await project_domain.is_alive(project_name):
        if await project_domain.validate_tags(
                project_name,
                tags):
            project_loader = info.context.loaders['project']
            project_attrs = await project_loader.load(project_name)
            project_attrs = project_attrs['attrs']
            project_tags = cast(ProjectType, project_attrs.get('tag', {}))
            project_tags = {'tag': project_tags}
            success = await _update_tags(
                project_name, project_tags, tags
            )
        else:
            util.cloudwatch_log(
                info.context,
                ('Security: Attempted to upload '
                 'tags without the allowed structure')  # pragma: no cover
            )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to upload tags '
             'without the allowed validations')  # pragma: no cover
        )
    if success:
        util.queue_cache_invalidation(f'tags*{project_name}')
        util.cloudwatch_log(
            info.context,
            ('Security: Added tag to '
             f'{project_name} project successfully')
        )
    project = await resolve(info, project_name, True, False)
    return SimpleProjectPayloadType(success=success, project=project)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_remove_tag(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        tag: str) -> SimpleProjectPayloadType:
    """Resolve remove_tag mutation."""
    success = False
    project_name = project_name.lower()
    if await project_domain.is_alive(project_name):
        project_loader = info.context.loaders['project']
        project_attrs = await project_loader.load(project_name)
        project_attrs = project_attrs['attrs']
        project_tags = cast(ProjectType, project_attrs.get('tag', {}))
        project_tags = {'tag': project_tags}
        cast(Set[str], project_tags.get('tag')).remove(tag)
        if project_tags.get('tag') == set():
            project_tags['tag'] = None
        tag_deleted = await project_domain.update(
            project_name, project_tags
        )
        if tag_deleted:
            success = True
        else:
            LOGGER.error('Couldn\'t remove a tag', extra={'extra': locals()})
    if success:
        util.queue_cache_invalidation(f'tags*{project_name}')
        util.cloudwatch_log(
            info.context,
            ('Security: Removed tag from '
             f'{project_name} project successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to remove '
             f'tag in {project_name} project')  # pragma: no cover
        )
    project = await resolve(info, project_name, True, False)
    return SimpleProjectPayloadType(success=success, project=project)


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve_projects(*_: Any) -> List[str]:
    """Resolve for ACTIVE and SUSPENDED projects."""
    return await project_domain.get_alive_projects()
