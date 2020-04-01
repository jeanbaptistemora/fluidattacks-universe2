# pylint: disable=import-error

from collections import defaultdict
import asyncio
import sys

from asgiref.sync import sync_to_async
from graphql import GraphQLError

from backend.decorators import (
    enforce_group_level_auth_async, get_entity_cache_async, rename_kwargs
)
from backend.domain import (
    comment as comment_domain,
    finding as finding_domain,
    user as user_domain,
    vulnerability as vuln_domain
)
from backend.utils import findings as finding_utils
from backend import util

from aiodataloader import DataLoader
from ariadne import convert_camel_case_to_snake


async def _batch_load_fn(finding_ids):
    """Batch the data load requests within the same execution fragment."""
    findings = defaultdict(list)

    for finding in await sync_to_async(finding_domain.get_findings)(
        finding_ids
    ):
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

    return [findings.get(finding_id, []) for finding_id in finding_ids]


# pylint: disable=too-few-public-methods
class FindingLoader(DataLoader):
    async def batch_load_fn(self, finding_ids):
        return await _batch_load_fn(finding_ids)


@get_entity_cache_async
async def _get_vulnerabilities(
    info, identifier, vuln_type=None, state=None, approval_status=None
):
    """Get vulnerabilities."""
    vuln_filtered = \
        await info.context.loaders['vulnerability'].load(identifier)
    if vuln_type:
        vuln_filtered = \
            [vuln for vuln in vuln_filtered if vuln.vuln_type == vuln_type
             and (vuln['current_approval_status'] != 'PENDING' or
                  vuln['last_approved_status'])]
    if state:
        vuln_filtered = \
            [vuln for vuln in vuln_filtered
             if vuln_domain.get_current_state(vuln) == state and
             (vuln['current_approval_status'] != 'PENDING' or
              vuln['last_approved_status'])]
    if approval_status:
        vuln_filtered = \
            {vuln for vuln in vuln_filtered
             if vuln['current_approval_status'] == approval_status}
    return dict(vulnerabilities=vuln_filtered)


@sync_to_async
def _get_id(_, identifier):
    """Get id."""
    return dict(id=identifier)


@get_entity_cache_async
async def _get_project_name(info, identifier):
    """Get project_name."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(project_name=finding['project_name'])


@get_entity_cache_async
async def _get_open_vulnerabilities(info, identifier):
    """Get open_vulnerabilities."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    open_vulnerabilities = len([
        vuln for vuln in vulns
        if await sync_to_async(vuln_domain.get_current_state)(vuln) == 'open'
        and
        (vuln['current_approval_status'] != 'PENDING' or
            vuln['last_approved_status'])])
    return dict(open_vulnerabilities=open_vulnerabilities)


@get_entity_cache_async
async def _get_closed_vulnerabilities(info, identifier):
    """Get closed_vulnerabilities."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    closed_vulnerabilities = len([
        vuln for vuln in vulns
        if await sync_to_async(vuln_domain.get_current_state)(vuln) == 'closed'
        and
        (vuln['current_approval_status'] != 'PENDING' or
            vuln['last_approved_status'])])
    return dict(closed_vulnerabilities=closed_vulnerabilities)


@get_entity_cache_async
async def _get_release_date(info, identifier):
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
    return dict(release_date=release_date)


@get_entity_cache_async
async def _get_tracking(info, identifier):
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
    return dict(tracking=tracking)


@get_entity_cache_async
async def _get_records(info, identifier):
    """Get records."""
    finding = await info.context.loaders['finding'].load(identifier)
    if finding['records']['url']:
        records = await sync_to_async(finding_utils.get_records_from_file)(
            finding['project_name'], finding['id'], finding['records']['url'])
    else:
        records = []
    return dict(records=records)


@get_entity_cache_async
async def _get_severity(info, identifier):
    """Get severity."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(severity=finding['severity'])


@get_entity_cache_async
async def _get_cvss_version(info, identifier):
    """Get cvss_version."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(cvss_version=finding['cvss_version'])


@get_entity_cache_async
async def _get_exploit(info, identifier):
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
    return dict(exploit=exploit)


@get_entity_cache_async
async def _get_evidence(info, identifier):
    """Get evidence."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(evidence=finding['evidence'])


@get_entity_cache_async
async def _get_comments(info, identifier):
    """Get comments."""
    finding = await info.context.loaders['finding'].load(identifier)
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    curr_user_role = \
        user_domain.get_group_level_role(user_email, finding['project_name'])
    comments = await sync_to_async(comment_domain.get_comments)(
        finding['id'], curr_user_role
    )
    return dict(comments=comments)


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_observations(info, identifier):
    """Get observations."""
    finding = await info.context.loaders['finding'].load(identifier)
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    curr_user_role = \
        user_domain.get_group_level_role(user_email, finding['project_name'])
    observations = await sync_to_async(comment_domain.get_observations)(
        finding['id'], curr_user_role
    )
    return dict(observations=observations)


@get_entity_cache_async
async def _get_state(info, identifier):
    """Get state."""
    vulns = await info.context.loaders['vulnerability'].load(identifier)

    state = 'open' \
        if [vuln for vuln in vulns
            if await sync_to_async(vuln_domain.get_last_approved_status)(vuln)
            == 'open'] \
        else 'closed'
    return dict(state=state)


@get_entity_cache_async
async def _get_last_vulnerability(info, identifier):
    """Get last_vulnerability."""
    finding = await info.context.loaders['finding'].load(identifier)
    last_vuln_date = \
        util.calculate_datediff_since(finding['last_vulnerability'])
    last_vulnerability = last_vuln_date.days
    return dict(last_vulnerability=last_vulnerability)


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_historic_state(info, identifier):
    """Get historic_state."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(historic_state=finding['historic_state'])


@get_entity_cache_async
async def _get_title(info, identifier):
    """Get title."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(title=finding['title'])


@get_entity_cache_async
async def _get_scenario(info, identifier):
    """Get scenario."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(scenario=finding['scenario'])


@get_entity_cache_async
async def _get_actor(info, identifier):
    """Get actor."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(actor=finding['actor'])


@get_entity_cache_async
async def _get_description(info, identifier):
    """Get description."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(description=finding['description'])


@get_entity_cache_async
async def _get_requirements(info, identifier):
    """Get requirements."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(requirements=finding['requirements'])


@get_entity_cache_async
async def _get_attack_vector_desc(info, identifier):
    """Get attack_vector_desc."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(attack_vector_desc=finding['attack_vector_desc'])


@get_entity_cache_async
async def _get_threat(info, identifier):
    """Get threat."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(threat=finding['threat'])


@get_entity_cache_async
async def _get_recommendation(info, identifier):
    """Get recommendation."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(recommendation=finding['recommendation'])


@get_entity_cache_async
async def _get_affected_systems(info, identifier):
    """Get affected_systems."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(affected_systems=finding['affected_systems'])


@get_entity_cache_async
async def _get_compromised_attributes(info, identifier):
    """Get compromised_attributes."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(compromised_attributes=finding['compromised_attributes'])


@get_entity_cache_async
async def _get_compromised_records(info, identifier):
    """Get compromised_records."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(compromised_records=finding['compromised_records'])


@get_entity_cache_async
async def _get_cwe_url(info, identifier):
    """Get cwe_url."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(cwe_url=finding['cwe_url'])


@get_entity_cache_async
async def _get_bts_url(info, identifier):
    """Get bts_url."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(bts_url=finding['bts_url'])


@get_entity_cache_async
async def _get_risk(info, identifier):
    """Get risk."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(risk=finding['risk'])


@get_entity_cache_async
async def _get_remediated(info, identifier):
    """Get remediated."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(remediated=finding['remediated'])


@get_entity_cache_async
async def _get_type(info, identifier):
    """Get type."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(type=finding['type'])


@get_entity_cache_async
async def _get_age(info, identifier):
    """Get age."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(age=finding['age'])


@get_entity_cache_async
async def _get_is_exploitable(info, identifier):
    """Get is_exploitable."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(is_exploitable=finding['is_exploitable'])


@get_entity_cache_async
async def _get_severity_score(info, identifier):
    """Get severity_score."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(severity_score=finding['severity_score'])


@get_entity_cache_async
async def _get_report_date(info, identifier):
    """Get report_date."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(report_date=finding['report_date'])


@rename_kwargs({'identifier': 'finding_id'})
@enforce_group_level_auth_async
@rename_kwargs({'finding_id': 'identifier'})
@get_entity_cache_async
async def _get_analyst(info, identifier):
    """Get analyst."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(analyst=finding['analyst'])


@get_entity_cache_async
async def _get_historic_treatment(info, identifier):
    """Get historic_treatment."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(historic_treatment=finding['historic_treatment'])


@get_entity_cache_async
async def _get_current_state(info, identifier):
    """Get current_state."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(current_state=finding['current_state'])


@get_entity_cache_async
async def _get_new_remediated(info, identifier):
    """Get new_remediated."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(new_remediated=finding['new_remediated'])


@get_entity_cache_async
async def _get_verified(info, identifier):
    """Get verified."""
    finding = await info.context.loaders['finding'].load(identifier)
    return dict(verified=finding['verified'])


async def resolve(info, identifier, as_field=False):
    """Async resolve fields."""
    result = dict()
    tasks = list()
    requested_fields = \
        util.get_requested_fields('findings',
                                  info.field_nodes[0].selection_set) \
        if as_field else info.field_nodes[0].selection_set.selections

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
        tasks.append(
            asyncio.ensure_future(resolver_func(info, **params))
        )
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result
