# pylint: disable=method-hidden

from collections import defaultdict
import sys
from typing import Dict, List

from graphql.language.ast import SelectionSetNode
from graphql import GraphQLError

from asgiref.sync import sync_to_async

from backend.decorators import (
    enforce_group_level_auth_async, get_entity_cache_async, rename_kwargs
)
from backend.domain import (
    comment as comment_domain,
    finding as finding_domain,
    user as user_domain,
    vulnerability as vuln_domain
)
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    Vulnerability as VulnerabilityType,
)
from backend.utils import findings as finding_utils
from backend import util

from aiodataloader import DataLoader
from ariadne import convert_camel_case_to_snake


async def _batch_load_fn(
        finding_ids: List[str]) -> List[Dict[str, FindingType]]:
    """Batch the data load requests within the same execution fragment."""
    findings: Dict[str, Dict[str, FindingType]] = \
        defaultdict(Dict[str, FindingType])

    fins = await finding_domain.get_findings_async(finding_ids)

    for finding in fins:
        findings[finding['findingId']] = dict(
            actor=finding.get('actor', ''),
            affected_systems=finding.get('affectedSystems', ''),
            age=finding.get('age', 0),
            analyst=finding.get('analyst', ''),
            attack_vector_desc=finding.get('attackVectorDesc', ''),
            bts_url=finding.get('externalBts', ''),
            compromised_attributes=finding.get('compromisedAttrs', ''),
            compromised_records=finding.get('recordsNumber', 0),
            cvss_version=finding.get('cvssVersion', '3.1'),
            cwe_url=finding.get('cwe', ''),
            description=finding.get('vulnerability', ''),
            evidence=finding.get('evidence', {}),
            exploit=finding.get('exploit', {}),
            id=finding.get('findingId', ''),
            is_exploitable=finding.get('exploitable', ''),
            last_vulnerability=finding.get('lastVulnerability', 0),
            project_name=finding.get('projectName', ''),
            recommendation=finding.get('effectSolution', ''),
            records=finding.get('records', {}),
            release_date=finding.get('releaseDate', ''),
            remediated=finding.get('remediated', False),
            new_remediated=finding.get('newRemediated', False),
            verified=finding.get('verified', False),
            report_date=finding.get('reportDate', ''),
            requirements=finding.get('requirements', ''),
            risk=finding.get('risk', ''),
            scenario=finding.get('scenario', ''),
            severity=finding.get('severity', {}),
            severity_score=finding.get('severityCvss', 0.0),
            threat=finding.get('threat', ''),
            title=finding.get('finding', ''),
            type=finding.get('findingType', ''),
            historic_state=finding.get('historicState', []),
            historic_treatment=finding.get('historicTreatment', []),
            current_state=finding.get(
                'historicState', [{}])[-1].get('state', '')
        )

    return [findings.get(finding_id, dict()) for finding_id in finding_ids]


# pylint: disable=too-few-public-methods
class FindingLoader(DataLoader):
    async def batch_load_fn(
            self, finding_ids: List[str]) -> List[Dict[str, FindingType]]:
        return await _batch_load_fn(finding_ids)


@get_entity_cache_async
async def _get_vulnerabilities(info, identifier: str,
                               state: str = '') -> List[VulnerabilityType]:
    """Get vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)
    if state:
        vuln_filtered = \
            [vuln for vuln in vuln_filtered
             if vuln['current_state'] == state and
             (vuln['current_approval_status'] != 'PENDING' or
              vuln['last_approved_status'])]
    return vuln_filtered


@get_entity_cache_async
async def _get_ports_vulns(info, identifier: str) -> List[VulnerabilityType]:
    """Get ports vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)

    vuln_filtered = \
        [vuln for vuln in vuln_filtered if vuln['vuln_type'] == 'ports'
            and (vuln['current_approval_status'] != 'PENDING' or
                 vuln['last_approved_status'])]
    return vuln_filtered


@get_entity_cache_async
async def _get_inputs_vulns(info, identifier: str) -> List[VulnerabilityType]:
    """Get inputs vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)

    vuln_filtered = \
        [vuln for vuln in vuln_filtered if vuln['vuln_type'] == 'inputs'
            and (vuln['current_approval_status'] != 'PENDING' or
                 vuln['last_approved_status'])]
    return vuln_filtered


@get_entity_cache_async
async def _get_lines_vulns(info, identifier: str) -> List[VulnerabilityType]:
    """Get lines vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)

    vuln_filtered = \
        [vuln for vuln in vuln_filtered if vuln['vuln_type'] == 'lines'
            and (vuln['current_approval_status'] != 'PENDING' or
                 vuln['last_approved_status'])]
    return vuln_filtered


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_pending_vulns(info, identifier: str) -> List[VulnerabilityType]:
    """Get pending vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)
    vuln_filtered = \
        [vuln for vuln in vuln_filtered
            if vuln['current_approval_status'] == 'PENDING']
    return vuln_filtered


@sync_to_async
def _get_id(_, identifier: str) -> str:
    """Get id."""
    return identifier


@get_entity_cache_async
async def _get_project_name(info, identifier: str) -> str:
    """Get project_name."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['project_name']


@get_entity_cache_async
async def _get_open_vulnerabilities(info, identifier: str) -> int:
    """Get open_vulnerabilities."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    open_vulnerabilities = len([
        vuln for vuln in vulns
        if vuln['current_state'] == 'open'
        and
        (vuln['current_approval_status'] != 'PENDING' or
            vuln['last_approved_status'])])
    return open_vulnerabilities


@get_entity_cache_async
async def _get_closed_vulnerabilities(info, identifier: str) -> int:
    """Get closed_vulnerabilities."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    closed_vulnerabilities = len([
        vuln for vuln in vulns
        if vuln['current_state'] == 'closed'
        and
        (vuln['current_approval_status'] != 'PENDING' or
            vuln['last_approved_status'])])
    return closed_vulnerabilities


@get_entity_cache_async
async def _get_release_date(info, identifier: str) -> str:
    """Get release date."""
    allowed_roles = ['admin', 'analyst']
    finding = await info.context.loaders['finding'].load(identifier)
    release_date = finding['release_date']
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    curr_user_role = \
        user_domain.get_group_level_role(user_email, finding['project_name'])
    if not release_date and curr_user_role not in allowed_roles:
        raise GraphQLError('Access denied')
    return release_date


@get_entity_cache_async
async def _get_tracking(info, identifier: str) -> List[Dict[str, int]]:
    """Get tracking."""
    finding = await info.context.loaders['finding'].load(identifier)
    release_date = finding['release_date']
    if release_date:
        vulns = await info.context.loaders['vulnerability'].load(identifier)
        tracking = \
            await \
            sync_to_async(finding_domain.get_tracking_vulnerabilities)(vulns)
    else:
        tracking = []
    return tracking


@get_entity_cache_async
async def _get_records(info, identifier: str) -> List[Dict[object, object]]:
    """Get records."""
    finding = await info.context.loaders['finding'].load(identifier)
    if finding['records']['url']:
        records = await sync_to_async(finding_utils.get_records_from_file)(
            finding['project_name'], finding['id'], finding['records']['url'])
    else:
        records = []
    return records


@get_entity_cache_async
async def _get_severity(info, identifier: str) -> Dict[str, str]:
    """Get severity."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['severity']


@get_entity_cache_async
async def _get_cvss_version(info, identifier: str) -> str:
    """Get cvss_version."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['cvss_version']


@get_entity_cache_async
async def _get_exploit(info, identifier: str) -> str:
    """Get exploit."""
    finding = await info.context.loaders['finding'].load(identifier)
    if finding['exploit']['url']:
        exploit = \
            await \
            sync_to_async(finding_utils.get_exploit_from_file)(
                finding['project_name'], finding['id'],
                finding['exploit']['url'])
    else:
        exploit = ''
    return exploit


@get_entity_cache_async
async def _get_evidence(info, identifier: str) -> Dict[str, Dict[str, str]]:
    """Get evidence."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['evidence']


@get_entity_cache_async
async def _get_comments(info, identifier: str) -> List[CommentType]:
    """Get comments."""
    finding = await info.context.loaders['finding'].load(identifier)
    finding_id = finding['id']
    project_name = finding.get('project_name')
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    comments = await sync_to_async(comment_domain.get_comments)(
        project_name, finding_id, user_email
    )
    return comments


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_observations(info, identifier: str) -> List[CommentType]:
    """Get observations."""
    finding = await info.context.loaders['finding'].load(identifier)
    finding_id = finding['id']
    project_name = finding['project_name']
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    observations = await sync_to_async(comment_domain.get_observations)(
        project_name, finding_id, user_email
    )
    return observations


@get_entity_cache_async
async def _get_state(info, identifier: str) -> str:
    """Get state."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    state = 'open' \
        if [vuln for vuln in vulns
            if await sync_to_async(vuln_domain.get_last_approved_status)(vuln)
            == 'open'] \
        else 'closed'
    return state


@get_entity_cache_async
async def _get_last_vulnerability(info, identifier: str) -> int:
    """Get last_vulnerability."""
    finding = await info.context.loaders['finding'].load(identifier)
    last_vuln_date = \
        util.calculate_datediff_since(finding['last_vulnerability'])
    return last_vuln_date.days


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_historic_state(info, identifier: str) -> List[Dict[str, str]]:
    """Get historic_state."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['historic_state']


@get_entity_cache_async
async def _get_title(info, identifier: str) -> str:
    """Get title."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['title']


@get_entity_cache_async
async def _get_scenario(info, identifier: str) -> str:
    """Get scenario."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['scenario']


@get_entity_cache_async
async def _get_actor(info, identifier: str) -> str:
    """Get actor."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['actor']


@get_entity_cache_async
async def _get_description(info, identifier: str) -> str:
    """Get description."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['description']


@get_entity_cache_async
async def _get_requirements(info, identifier: str) -> str:
    """Get requirements."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['requirements']


@get_entity_cache_async
async def _get_attack_vector_desc(info, identifier: str) -> str:
    """Get attack_vector_desc."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['attack_vector_desc']


@get_entity_cache_async
async def _get_threat(info, identifier: str) -> str:
    """Get threat."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['threat']


@get_entity_cache_async
async def _get_recommendation(info, identifier: str) -> str:
    """Get recommendation."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['recommendation']


@get_entity_cache_async
async def _get_affected_systems(info, identifier: str) -> str:
    """Get affected_systems."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['affected_systems']


@get_entity_cache_async
async def _get_compromised_attributes(info, identifier: str) -> str:
    """Get compromised_attributes."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['compromised_attributes']


@get_entity_cache_async
async def _get_compromised_records(info, identifier: str) -> int:
    """Get compromised_records."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['compromised_records']


@get_entity_cache_async
async def _get_cwe_url(info, identifier: str) -> str:
    """Get cwe_url."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['cwe_url']


@get_entity_cache_async
async def _get_bts_url(info, identifier: str) -> str:
    """Get bts_url."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['bts_url']


@get_entity_cache_async
async def _get_risk(info, identifier: str) -> str:
    """Get risk."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['risk']


@get_entity_cache_async
async def _get_remediated(info, identifier: str) -> bool:
    """Get remediated."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['remediated']


@get_entity_cache_async
async def _get_type(info, identifier: str) -> str:
    """Get type."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['type']


@get_entity_cache_async
async def _get_age(info, identifier: str) -> int:
    """Get age."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['age']


@get_entity_cache_async
async def _get_is_exploitable(info, identifier: str) -> bool:
    """Get is_exploitable."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['is_exploitable']


@get_entity_cache_async
async def _get_severity_score(info, identifier: str) -> float:
    """Get severity_score."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['severity_score']


@get_entity_cache_async
async def _get_report_date(info, identifier: str) -> str:
    """Get report_date."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['report_date']


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_analyst(info, identifier: str) -> str:
    """Get analyst."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['analyst']


@get_entity_cache_async
async def _get_historic_treatment(info,
                                  identifier: str) -> List[Dict[str, str]]:
    """Get historic_treatment."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['historic_treatment']


@get_entity_cache_async
async def _get_current_state(info, identifier: str) -> str:
    """Get current_state."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['current_state']


@get_entity_cache_async
async def _get_new_remediated(info, identifier: str) -> bool:
    """Get new_remediated."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['new_remediated']


@get_entity_cache_async
async def _get_verified(info, identifier: str) -> bool:
    """Get verified."""
    finding = await info.context.loaders['finding'].load(identifier)
    return finding['verified']


async def resolve(
        info, identifier: str, as_field: bool = False,
        selection_set: SelectionSetNode = SelectionSetNode()) -> \
        Dict[str, FindingType]:
    """Async resolve fields."""
    result = dict()
    requested_fields = \
        selection_set.selections if as_field else \
        info.field_nodes[0].selection_set.selections

    for requested_field in requested_fields:
        if util.is_skippable(info, requested_field):
            continue
        params = {
            'identifier': identifier
        }
        field_params = util.get_field_parameters(requested_field)
        if field_params:
            params.update(field_params)
        requested_field = \
            convert_camel_case_to_snake(requested_field.name.value)
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = resolver_func(info, **params)
    return result
