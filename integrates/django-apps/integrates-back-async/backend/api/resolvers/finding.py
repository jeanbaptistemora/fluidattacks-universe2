# pylint:disable=too-many-lines
from datetime import datetime
import logging
import sys
from time import time
from typing import Dict, List, Any, Union, cast

# Third party libraries
from ariadne import convert_camel_case_to_snake, convert_kwargs_to_snake_case
from asgiref.sync import sync_to_async
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphql.language.ast import (
    SelectionSetNode,
)
from graphql.type.definition import GraphQLResolveInfo
from graphql import GraphQLError

from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async, get_entity_cache_async, rename_kwargs,
    require_forces, require_integrates,
    require_login, require_finding_access
)
from backend.domain import (
    comment as comment_domain,
    finding as finding_domain,
    organization as org_domain,
    vulnerability as vuln_domain
)
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    SimplePayload as SimplePayloadType,
    SimpleFindingPayload as SimpleFindingPayloadType,
    ApproveDraftPayload as ApproveDraftPayloadType,
    AddCommentPayload as AddCommentPayloadType,
    AddConsultPayload as AddConsultPayloadType,
    Vulnerability as VulnerabilityType,
)
from backend.utils import (
    findings as finding_utils,
)
from backend import authz, util
from fluidintegrates.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@get_entity_cache_async
async def _get_vulnerabilities(
        info: GraphQLResolveInfo,
        identifier: str,
        state: str = '') -> List[VulnerabilityType]:
    """Get vulnerabilities."""
    vuln_filtered = await info.context.loaders['vulnerability'].load(
        identifier
    )
    if state:
        vuln_filtered = [
            vuln
            for vuln in vuln_filtered
            if (vuln['current_state'] == state and
                (vuln['current_approval_status'] != 'PENDING' or
                 vuln['last_approved_status']))
        ]
    return cast(List[VulnerabilityType], vuln_filtered)


@get_entity_cache_async
async def _get_ports_vulns(
        info: GraphQLResolveInfo,
        identifier: str) -> List[VulnerabilityType]:
    """Get ports vulnerabilities."""
    vuln_filtered = await info.context.loaders['vulnerability'].load(
        identifier
    )

    vuln_filtered = [
        vuln
        for vuln in vuln_filtered
        if (vuln['vuln_type'] == 'ports' and
            (vuln['current_approval_status'] != 'PENDING' or
             vuln['last_approved_status']))
    ]
    return cast(List[VulnerabilityType], vuln_filtered)


@get_entity_cache_async
async def _get_inputs_vulns(
        info: GraphQLResolveInfo,
        identifier: str) -> List[VulnerabilityType]:
    """Get inputs vulnerabilities."""
    vuln_filtered = await info.context.loaders['vulnerability'].load(
        identifier
    )

    vuln_filtered = [
        vuln
        for vuln in vuln_filtered
        if (vuln['vuln_type'] == 'inputs' and
            (vuln['current_approval_status'] != 'PENDING' or
             vuln['last_approved_status']))
    ]
    return cast(List[VulnerabilityType], vuln_filtered)


@get_entity_cache_async
async def _get_lines_vulns(
        info: GraphQLResolveInfo,
        identifier: str) -> List[VulnerabilityType]:
    """Get lines vulnerabilities."""
    vuln_filtered = await info.context.loaders['vulnerability'].load(
        identifier
    )

    vuln_filtered = [
        vuln
        for vuln in vuln_filtered
        if (vuln['vuln_type'] == 'lines' and
            (vuln['current_approval_status'] != 'PENDING' or
             vuln['last_approved_status']))
    ]
    return cast(List[VulnerabilityType], vuln_filtered)


@rename_kwargs({'identifier': 'finding_id'})
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_pending_vulns(
        info: GraphQLResolveInfo,
        identifier: str) -> List[VulnerabilityType]:
    """Get pending vulnerabilities."""
    vuln_filtered = await info.context.loaders['vulnerability'].load(
        identifier
    )
    vuln_filtered = [
        vuln
        for vuln in vuln_filtered
        if vuln['current_approval_status'] == 'PENDING'
    ]
    return cast(List[VulnerabilityType], vuln_filtered)


@sync_to_async  # type: ignore
def _get_id(_: GraphQLResolveInfo, identifier: str) -> str:
    """Get id."""
    return identifier


@get_entity_cache_async
async def _get_project_name(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get project_name."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['project_name'])


@get_entity_cache_async
async def _get_open_vulnerabilities(
        info: GraphQLResolveInfo,
        identifier: str) -> int:
    """Get open_vulnerabilities."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    open_vulnerabilities = len(vuln_domain.filter_open_vulnerabilities(vulns))

    return open_vulnerabilities


@get_entity_cache_async
async def _get_closed_vulnerabilities(
        info: GraphQLResolveInfo,
        identifier: str) -> int:
    """Get closed_vulnerabilities."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    closed_vulnerabilities = len([
        vuln
        for vuln in vulns
        if (vuln['current_state'] == 'closed' and
            (vuln['current_approval_status'] != 'PENDING' or
             vuln['last_approved_status']))
    ])
    return closed_vulnerabilities


@get_entity_cache_async
async def _get_release_date(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get release date."""
    allowed_roles = ['admin', 'analyst', 'group_manager', 'reviewer']
    finding = await info.context.loaders['finding'].load(identifier)
    release_date = finding['release_date']
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    curr_user_role = await authz.get_group_level_role(
        user_email, finding['project_name']
    )
    if not release_date and curr_user_role not in allowed_roles:
        raise GraphQLError('Access denied')
    return cast(str, release_date)


@get_entity_cache_async
async def _get_tracking(
        info: GraphQLResolveInfo,
        identifier: str) -> List[Dict[str, Union[str, int]]]:
    """Get tracking."""
    finding = await info.context.loaders['finding'].load(identifier)
    release_date = finding['release_date']
    if release_date:
        vulns = await info.context.loaders['vulnerability'].load(identifier)
        tracking = await finding_domain.get_tracking_vulnerabilities(vulns)
    else:
        tracking = []
    return tracking


@get_entity_cache_async
async def _get_records(
        info: GraphQLResolveInfo,
        identifier: str) -> List[Dict[object, object]]:
    """Get records."""
    finding = await info.context.loaders['finding'].load(identifier)
    if finding['records']['url']:
        records = await finding_utils.get_records_from_file(
            finding['project_name'], finding['id'], finding['records']['url'])
    else:
        records = []
    return records


@get_entity_cache_async
async def _get_severity(
        info: GraphQLResolveInfo,
        identifier: str) -> Dict[str, str]:
    """Get severity."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(Dict[str, str], finding['severity'])


@get_entity_cache_async
async def _get_cvss_version(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get cvss_version."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['cvss_version'])


@rename_kwargs({'identifier': 'finding_id'})
@require_forces
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_exploit(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get exploit."""
    finding = await info.context.loaders['finding'].load(identifier)
    if finding['exploit']['url']:
        exploit = await finding_utils.get_exploit_from_file(
            finding['project_name'],
            finding['id'],
            finding['exploit']['url']
        )
    else:
        exploit = ''
    return exploit


@get_entity_cache_async
async def _get_evidence(
        info: GraphQLResolveInfo,
        identifier: str) -> Dict[str, Dict[str, str]]:
    """Get evidence."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(Dict[str, Dict[str, str]], finding['evidence'])


@get_entity_cache_async
async def _get_comments(
        info: GraphQLResolveInfo,
        identifier: str) -> List[CommentType]:
    """Get comments."""
    finding = await info.context.loaders['finding'].load(identifier)
    finding_id = finding['id']
    project_name = finding.get('project_name')
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    comments = await comment_domain.get_comments(
        project_name, finding_id, user_email
    )
    return comments


@get_entity_cache_async
async def _get_consulting(
        info: GraphQLResolveInfo,
        identifier: str) -> List[CommentType]:
    finding = await info.context.loaders['finding'].load(identifier)
    finding_id = finding['id']
    project_name = finding.get('project_name')
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    consultings = await comment_domain.get_comments(
        project_name, finding_id, user_email
    )
    return consultings


@rename_kwargs({'identifier': 'finding_id'})
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_observations(
        info: GraphQLResolveInfo,
        identifier: str) -> List[CommentType]:
    """Get observations."""
    finding = await info.context.loaders['finding'].load(identifier)
    finding_id = finding['id']
    project_name = finding['project_name']
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    observations = await comment_domain.get_observations(
        project_name, finding_id, user_email
    )
    return observations


@get_entity_cache_async
async def _get_state(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get state."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    state = (
        'open'
        if [
            vuln
            for vuln in vulns
            if vuln['last_approved_status'] == 'open'
        ]
        else 'closed'
    )
    return state


@get_entity_cache_async
async def _get_last_vulnerability(
        info: GraphQLResolveInfo,
        identifier: str) -> int:
    """Get last_vulnerability."""
    finding = await info.context.loaders['finding'].load(identifier)
    last_vuln_date = util.calculate_datediff_since(
        finding['last_vulnerability']
    )
    return last_vuln_date.days


@rename_kwargs({'identifier': 'finding_id'})
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_historic_state(
        info: GraphQLResolveInfo,
        identifier: str) -> List[Dict[str, str]]:
    """Get historic_state."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(List[Dict[str, str]], finding['historic_state'])


@get_entity_cache_async
async def _get_title(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get title."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['title'])


@get_entity_cache_async
async def _get_scenario(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get scenario."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['scenario'])


@get_entity_cache_async
async def _get_actor(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get actor."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['actor'])


@get_entity_cache_async
async def _get_description(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get description."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['description'])


@get_entity_cache_async
async def _get_requirements(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get requirements."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['requirements'])


@get_entity_cache_async
async def _get_attack_vector_desc(
        info: GraphQLResolveInfo,
        identifier: str) -> str:
    """Get attack_vector_desc."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['attack_vector_desc'])


@get_entity_cache_async
async def _get_threat(
        info: GraphQLResolveInfo,
        identifier: str) -> str:
    """Get threat."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['threat'])


@get_entity_cache_async
async def _get_recommendation(
        info: GraphQLResolveInfo,
        identifier: str) -> str:
    """Get recommendation."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['recommendation'])


@get_entity_cache_async
async def _get_affected_systems(
        info: GraphQLResolveInfo,
        identifier: str) -> str:
    """Get affected_systems."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['affected_systems'])


@get_entity_cache_async
async def _get_compromised_attributes(
        info: GraphQLResolveInfo,
        identifier: str) -> str:
    """Get compromised_attributes."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['compromised_attributes'])


@get_entity_cache_async
async def _get_compromised_records(
        info: GraphQLResolveInfo,
        identifier: str) -> int:
    """Get compromised_records."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(int, finding['compromised_records'])


@get_entity_cache_async
async def _get_cwe_url(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get cwe_url."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['cwe_url'])


@get_entity_cache_async
async def _get_bts_url(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get bts_url."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['bts_url'])


@get_entity_cache_async
async def _get_risk(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get risk."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['risk'])


@get_entity_cache_async
async def _get_remediated(info: GraphQLResolveInfo, identifier: str) -> bool:
    """Get remediated."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(bool, finding['remediated'])


@get_entity_cache_async
async def _get_type(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get type."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['type'])


@get_entity_cache_async
async def _get_age(info: GraphQLResolveInfo, identifier: str) -> int:
    """Get age."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(int, finding['age'])


@get_entity_cache_async
async def _get_is_exploitable(
        info: GraphQLResolveInfo,
        identifier: str) -> bool:
    """Get is_exploitable."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(bool, finding['is_exploitable'])


@get_entity_cache_async
async def _get_severity_score(
        info: GraphQLResolveInfo,
        identifier: str) -> float:
    """Get severity_score."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(float, finding['severity_score'])


@get_entity_cache_async
async def _get_report_date(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get report_date."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['report_date'])


@rename_kwargs({'identifier': 'finding_id'})
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_analyst(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get analyst."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['analyst'])


@get_entity_cache_async
async def _get_historic_treatment(
        info: GraphQLResolveInfo,
        identifier: str) -> List[Dict[str, str]]:
    """Get historic_treatment."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(List[Dict[str, str]], finding['historic_treatment'])


@get_entity_cache_async
async def _get_current_state(info: GraphQLResolveInfo, identifier: str) -> str:
    """Get current_state."""
    finding = await info.context.loaders['finding'].load(identifier)
    return cast(str, finding['current_state'])


@get_entity_cache_async
async def _get_new_remediated(
        info: GraphQLResolveInfo,
        identifier: str) -> bool:
    """Get new_remediated."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)
    open_vulns = [
        vuln
        for vuln in vulns
        if vuln['last_approved_status'] == 'open'
    ]
    remediated_vulns = [vuln for vuln in vulns if vuln['remediated']]
    new_remediated = len(remediated_vulns) == len(open_vulns)
    return new_remediated


@get_entity_cache_async
async def _get_verified(info: GraphQLResolveInfo, identifier: str) -> bool:
    """Get verified."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)
    remediated_vulns = [
        vuln
        for vuln in vulns
        if vuln['last_approved_status'] == 'open' and vuln['remediated']
    ]
    verified = len(remediated_vulns) == 0
    return verified


async def resolve(
    info: GraphQLResolveInfo,
    identifier: str,
    as_field: bool = False,
    selection_set: SelectionSetNode = SelectionSetNode()
) -> Dict[str, FindingType]:
    """Async resolve fields."""
    result = dict()
    requested_fields = (
        selection_set.selections
        if as_field
        else info.field_nodes[0].selection_set.selections
    )

    for requested_field in requested_fields:
        if util.is_skippable(info, requested_field):
            continue
        params = {
            'identifier': identifier
        }
        field_params = util.get_field_parameters(requested_field)
        if field_params:
            params.update(field_params)
        requested_field = convert_camel_case_to_snake(
            requested_field.name.value
        )
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = resolver_func(info, **params)
    return result


@convert_kwargs_to_snake_case  # type: ignore
def resolve_finding_mutation(
        obj: Any,
        info: GraphQLResolveInfo,
        **parameters: Any
) -> Union[
    SimpleFindingPayloadType,
    SimplePayloadType,
    AddCommentPayloadType,
    ApproveDraftPayloadType
]:
    """Resolve findings mutation."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return cast(
        Union[
            SimpleFindingPayloadType,
            SimplePayloadType,
            AddCommentPayloadType,
            ApproveDraftPayloadType
        ],
        resolver_func(obj, info, **parameters)
    )


@convert_kwargs_to_snake_case  # type: ignore
@rename_kwargs({'identifier': 'finding_id'})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
@rename_kwargs({'finding_id': 'identifier'})
async def resolve_finding(
        _: Any,
        info: GraphQLResolveInfo,
        identifier: str) -> Dict[str, FindingType]:
    """Resolve finding query."""
    return await resolve(info, identifier)


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
async def _do_update_evidence(
        _: Any,
        info: GraphQLResolveInfo,
        evidence_id: str,
        finding_id: str,
        file: InMemoryUploadedFile) -> SimplePayloadType:
    """Resolve update_evidence mutation."""
    success = False

    if await sync_to_async(finding_domain.validate_evidence)(
        evidence_id, file
    ):
        success = await finding_domain.update_evidence(
            finding_id, evidence_id, file
        )

    if success:
        await util.invalidate_cache(
            f'evidence*{finding_id}',
            f'records*{finding_id}'
        )
        util.cloudwatch_log(
            info.context,
            ('Security: Updated evidence in finding '
             f'{finding_id} successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to update evidence in '
             f'finding {finding_id}')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def _do_update_evidence_description(
        _: Any,
        info: GraphQLResolveInfo,
        finding_id: str,
        evidence_id: str,
        description: str) -> SimplePayloadType:
    """Resolve update_evidence_description mutation."""
    success = False
    try:
        success = await finding_domain.update_evidence_description(
            finding_id, evidence_id, description
        )
        if success:
            util.queue_cache_invalidation(f'evidence*{finding_id}')
            util.cloudwatch_log(
                info.context,
                ('Security: Evidence description '
                 'successfully updated in finding '
                 f'{finding_id}')  # pragma: no cover
            )
        else:
            util.cloudwatch_log(
                info.context,
                ('Security: Attempted to update '
                 f'evidence description in {finding_id}')  # pragma: no cover
            )
    except KeyError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def _do_update_severity(
        _: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> SimpleFindingPayloadType:
    """Perform update_severity mutation."""
    data = parameters.get('data', dict())
    data = {util.snakecase_to_camelcase(k): data[k] for k in data}
    finding_id = parameters.get('finding_id', '')
    finding_loader = info.context.loaders['finding']
    finding_data = await finding_loader.load(finding_id)
    project_name = finding_data['project_name']
    success = False
    success = await finding_domain.save_severity(data)
    if success:
        util.queue_cache_invalidation(
            f'severity*{finding_id}',
            f'severity*{project_name}'
        )
        util.cloudwatch_log(
            info.context,
            ('Security: Updated severity in '
             f'finding {finding_id} successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to update '
             f'severity in finding {finding_id}')  # pragma: no cover
        )
    finding = await info.context.loaders['finding'].load(finding_id)
    return SimpleFindingPayloadType(finding=finding, success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def _do_add_finding_comment(
        _: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> AddCommentPayloadType:
    """Perform add_finding_comment mutation."""
    param_type = parameters.get('type', '').lower()
    if param_type in ['comment', 'observation']:
        user_data = await util.get_jwt_content(info.context)
        user_email = user_data['user_email']
        finding_id = str(parameters.get('finding_id'))
        finding_loader = info.context.loaders['finding']
        finding = await finding_loader.load(finding_id)
        group = finding.get('project_name')
        role = await authz.get_group_level_role(user_email, group)
        if (param_type == 'observation' and
                role not in ['analyst', 'admin', 'group_manager', 'reviewer']):
            util.cloudwatch_log(
                info.context,
                ('Security: Unauthorized role '
                 'attempted to add observation')  # pragma: no cover
            )
            raise GraphQLError('Access denied')

        user_email = user_data['user_email']
        comment_id = int(round(time() * 1000))
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_data = {
            'user_id': comment_id,
            'comment_type': param_type,
            'content': parameters.get('content'),
            'fullname': ' '.join(
                [user_data['first_name'], user_data['last_name']]
            ),
            'parent': parameters.get('parent'),
            'created': current_time,
            'modified': current_time,
        }
        success = await finding_domain.add_comment(
            user_email=user_email,
            comment_data=comment_data,
            finding_id=finding_id
        )
    else:
        raise GraphQLError('Invalid comment type')

    if success:
        util.queue_cache_invalidation(f'{param_type}*{finding_id}')
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
    ret = AddCommentPayloadType(success=success, comment_id=str(comment_id))
    return ret


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
    param_type = parameters.get('type', '').lower()
    if param_type in ['consult', 'observation']:
        user_data = await util.get_jwt_content(info.context)
        user_email = user_data['user_email']
        finding_id = str(parameters.get('finding_id'))
        finding_loader = info.context.loaders['finding']
        finding = await finding_loader.load(finding_id)
        group = finding.get('project_name')
        role = await authz.get_group_level_role(user_email, group)
        if (param_type == 'observation' and
                role not in ['analyst', 'admin', 'group_manager', 'reviewer']):
            util.cloudwatch_log(
                info.context,
                ('Security: Unauthorized role '
                 'attempted to add observation')  # pragma: no cover
            )
            raise GraphQLError('Access denied')

        user_email = user_data['user_email']
        comment_id = int(round(time() * 1000))
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_data = {
            'user_id': comment_id,
            'comment_type':
                'comment' if param_type == 'consult' else param_type,
            'content': parameters.get('content'),
            'fullname': ' '.join(
                [user_data['first_name'], user_data['last_name']]
            ),
            'parent': parameters.get('parent'),
            'created': current_time,
            'modified': current_time,
        }
        success = await finding_domain.add_comment(
            user_email=user_email,
            comment_data=comment_data,
            finding_id=finding_id
        )
    else:
        raise GraphQLError('Invalid comment type')
    if success:
        util.queue_cache_invalidation(f'{param_type}*{finding_id}')
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
async def _do_handle_acceptation(
        _: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> SimplePayloadType:
    """Resolve handle_acceptation mutation."""
    user_info = await util.get_jwt_content(info.context)
    user_mail = user_info['user_email']
    project_name = parameters.get('project_name', '')
    finding_id = parameters.get('finding_id', '')
    finding_loader = info.context.loaders['finding']
    finding_data = await finding_loader.load(finding_id)
    historic_treatment = finding_data.get('historic_treatment', [{}])
    if historic_treatment[-1]['acceptance_status'] != 'SUBMITTED':
        raise GraphQLError(
            'It cant be approved/rejected a finding'
            'definite assumption without being requested'
        )
    success = await finding_domain.handle_acceptation(
        finding_id,
        str(parameters.get('observations')),
        user_mail,
        str(parameters.get('response'))
    )
    if success:
        attrs_to_clean = {
            'historic_treatment': finding_id,
            'current_state': finding_id,
            'open_vulnerabilities': project_name,
            'drafts': project_name,
            'open_findings': project_name,
            'max*severity': project_name,
            'mean_remediate': project_name,
            'total_findings': project_name,
            'total_treatment': project_name
        }
        to_clean = util.format_cache_keys_pattern(attrs_to_clean)
        util.queue_cache_invalidation(*to_clean)
        util.forces_trigger_deployment(parameters.get('project_name', ''))
        util.cloudwatch_log(
            info.context,
            ('Security: Verified a request '
             f'in finding_id: {finding_id}')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


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
async def _do_update_client_description(
    _: Any,
    info: GraphQLResolveInfo,
    finding_id: str,
    **parameters: Any
) -> SimpleFindingPayloadType:
    """
    Perform update_client_description mutation.
    """
    finding_loader = info.context.loaders['finding']
    finding = await finding_loader.load(finding_id)
    project_name = finding['project_name']
    organization = await org_domain.get_id_for_group(project_name)
    user_info = await util.get_jwt_content(info.context)
    user_mail = user_info['user_email']
    finding_info_to_check = {
        'bts_url': finding['bts_url'],
        'historic_treatment': finding['historic_treatment'],
        'severity': finding['severity_score']
    }
    success = await finding_domain.update_client_description(
        finding_id,
        parameters,
        organization,
        finding_info_to_check,
        user_mail
    )
    if success:
        attrs_to_clean = {attribute: finding_id for attribute in parameters}
        to_clean = util.format_cache_keys_pattern(attrs_to_clean)
        util.queue_cache_invalidation(*to_clean)
        util.forces_trigger_deployment(project_name)
        util.cloudwatch_log(
            info.context,
            ('Security: Updated treatment in '
             f'finding {finding_id} successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to update '
             f'treatment in finding {finding_id}')  # pragma: no cover
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


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def _do_delete_finding(
        _: Any,
        info: GraphQLResolveInfo,
        finding_id: str,
        justification: str) -> SimplePayloadType:
    """Resolve delete_finding mutation."""
    finding_loader = info.context.loaders['finding']
    finding_data = await finding_loader.load(finding_id)
    project_name = finding_data['project_name']

    success = await finding_domain.delete_finding(
        finding_id, project_name, justification, info.context
    )
    if success:
        project_attrs_to_clean = {
            'severity': project_name,
            'finding': project_name,
            'drafts': project_name,
            'vuln': project_name
        }
        to_clean = util.format_cache_keys_pattern(project_attrs_to_clean)
        util.queue_cache_invalidation(*to_clean, finding_id)
        util.forces_trigger_deployment(project_name)
        util.cloudwatch_log(
            info.context,
            ('Security: Deleted finding: '
             f'{finding_id} successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to delete '
             f'finding: {finding_id}')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_approve_draft(
        _: Any,
        info: GraphQLResolveInfo,
        draft_id: str) -> ApproveDraftPayloadType:
    """Resolve approve_draft mutation."""
    user_info = await util.get_jwt_content(info.context)
    reviewer_email = user_info['user_email']
    project_name = await finding_domain.get_project(draft_id)

    success, release_date = await finding_domain.approve_draft(
        draft_id, reviewer_email
    )
    if success:
        project_attrs_to_clean = {
            'severity': project_name,
            'finding': project_name,
            'drafts': project_name,
            'vuln': project_name
        }
        to_clean = util.format_cache_keys_pattern(project_attrs_to_clean)
        util.queue_cache_invalidation(draft_id, *to_clean)
        util.forces_trigger_deployment(project_name)
        util.cloudwatch_log(
            info.context,
            ('Security: Approved draft in '
             f'{project_name} project successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to approve '
             f'draft in {project_name} project')  # pragma: no cover
        )
    return ApproveDraftPayloadType(release_date=release_date, success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_create_draft(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        title: str,
        **kwargs: Any) -> SimplePayloadType:
    """Resolve create_draft mutation."""
    success = await finding_domain.create_draft(
        info, project_name, title, **kwargs
    )
    if success:
        util.cloudwatch_log(
            info.context,
            ('Security: Created draft in '
             f'{project_name} project successfully')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def _do_submit_draft(
        _: Any,
        info: GraphQLResolveInfo,
        finding_id: str) -> SimplePayloadType:
    """Resolve submit_draft mutation."""
    user_info = await util.get_jwt_content(info.context)
    analyst_email = user_info['user_email']
    success = await finding_domain.submit_draft(finding_id, analyst_email)

    if success:
        util.queue_cache_invalidation(finding_id)
        util.cloudwatch_log(
            info.context,
            ('Security: Submitted draft '
             f'{finding_id} successfully')  # pragma: no cover
        )
    return SimplePayloadType(success=success)
