"""Domain functions for vulnerabilities."""   # pylint:disable=too-many-lines

# Standard libraries
import copy
import html
import html.parser
import logging
import logging.config
import uuid
from contextlib import AsyncExitStack
from itertools import zip_longest
from operator import itemgetter
from time import time
from typing import (
    Any,
    cast,
    Collection,
    Dict,
    List,
    Iterable,
    Optional,
    Set,
    Union,
)

# Third party libraries
import aioboto3
import yaml
from aioextensions import (
    collect,
    in_process,
    schedule,
)
from graphql.type.definition import GraphQLResolveInfo
from starlette.datastructures import UploadFile

# Local libraries
from back.settings import (
    LOGGING,
    NOEXTRA
)
from backend import (
    mailer,
    util,
)
from backend.typing import (
    Finding as FindingType,
    Historic,
    User as UserType,
    Vulnerability as VulnerabilityType,
)
from comments import domain as comments_domain
from custom_exceptions import (
    AlreadyZeroRiskRequested,
    InvalidJustificationMaxLength,
    NotZeroRiskRequested,
    VulnNotFound,
    VulnNotInFinding,
)
from dynamodb.operations_legacy import start_context
from group_access import domain as group_access_domain
from newutils import (
    datetime as datetime_utils,
    validations,
    vulnerabilities as vulns_utils,
)
from notifications import domain as notifications_domain
from vulnerabilities import dal as vulns_dal
from __init__ import BASE_URL


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def confirm_zero_risk_vulnerabilities(
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    vuln_ids: List[str]
) -> bool:
    validate_justificaiton_length(justification)
    vulnerabilities = await get_by_finding_and_uuids(finding_id, set(vuln_ids))
    vulnerabilities = [
        validate_requested_zero_risk_vuln(vuln)
        for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = int(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_email: str = user_info['user_email']
    comment_data = {
        'comment_type': 'zero_risk',
        'content': justification,
        'parent': 0,
        'user_id': comment_id
    }
    create_comment = await comments_domain.create(
        int(finding_id),
        comment_data,
        user_info
    )
    confirm_zero_risk_vulns = await collect(
        [
            vulns_dal.confirm_zero_risk_vulnerability(
                user_email,
                today,
                comment_id,
                vuln
            )
            for vuln in vulnerabilities
        ]
    )
    success = all(confirm_zero_risk_vulns) and create_comment[1]
    if not success:
        LOGGER.error('An error occurred confirming zero risk vuln', **NOEXTRA)
    return success


async def delete_tags(
    finding_id: str,
    vulnerabilities: List[str],
    tag: str
) -> bool:
    vuln_update_coroutines = []
    vuln_info = await get_by_finding_and_uuids(
        finding_id,
        set(vulnerabilities)
    )
    for index, vulnerability in enumerate(vulnerabilities):
        tag_info: Dict[str, Optional[Set[str]]] = {'tag': set()}
        if tag:
            if vuln_info[index]:
                tag_info['tag'] = cast(
                    Set[str],
                    vuln_info[index].get('tag', [])
                )
            if tag in cast(Set[str], tag_info.get('tag', [])):
                cast(Set[str], tag_info.get('tag')).remove(tag)
        if tag_info.get('tag') == set():
            tag_info['tag'] = None
        vuln_update_coroutines.append(
            vulns_dal.update(
                finding_id,
                vulnerability,
                cast(Dict[str, FindingType], tag_info)
            )
        )
    success = await collect(vuln_update_coroutines)
    return all(success)


async def delete_vulnerability(  # pylint: disable=too-many-arguments
    context: Any,
    finding_id: str,
    vuln_id: str,
    justification: str,
    user_email: str,
    source: str,
    include_closed_vuln: bool = False
) -> bool:
    vulnerability_loader = context.vulnerability
    vulnerability = await vulnerability_loader.load(vuln_id)
    success = False
    if vulnerability and vulnerability['historic_state']:
        all_states = cast(
            List[Dict[str, str]],
            vulnerability['historic_state']
        )
        current_state = all_states[-1].get('state')
        if current_state == 'open' or include_closed_vuln:
            current_day = datetime_utils.get_now_as_str()
            new_state = {
                'analyst': user_email,
                'date': current_day,
                'justification': justification,
                'source': source,
                'state': 'DELETED',
            }
            all_states.append(new_state)
            success = await vulns_dal.update(
                finding_id,
                str(vulnerability['id']),
                {'historic_state': all_states}
            )
    return success


def filter_closed_vulnerabilities(
    vulnerabilities: List[VulnerabilityType],
) -> List[VulnerabilityType]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability['current_state'] == 'closed'
    ]


def filter_confirmed_zero_risk(
    vulnerabilities: List[Dict[str, FindingType]],
) -> List[Dict[str, FindingType]]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if cast(
            Historic,
            vulnerability.get('historic_zero_risk', [{}])
        )[-1].get('status', '') == 'CONFIRMED'
    ]


def filter_non_confirmed_zero_risk_vuln(
    vulnerabilities: List[VulnerabilityType],
) -> List[VulnerabilityType]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability['zero_risk'] != 'Confirmed'
    ]


def filter_non_requested_zero_risk_vuln(
    vulnerabilities: List[VulnerabilityType],
) -> List[VulnerabilityType]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability['zero_risk'] != 'Requested'
    ]


def filter_open_vulnerabilities(
    vulnerabilities: List[VulnerabilityType],
) -> List[VulnerabilityType]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability['current_state'] == 'open'
    ]


def filter_remediated(
    vulnerabilities: List[VulnerabilityType],
) -> List[VulnerabilityType]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability['remediated']
    ]


def filter_requested_zero_risk(
    vulnerabilities: List[Dict[str, FindingType]],
) -> List[Dict[str, FindingType]]:
    return [
        vulnerability
        for vulnerability in vulnerabilities
        if cast(
            Historic,
            vulnerability.get('historic_zero_risk', [{}])
        )[-1].get('status', '') == 'REQUESTED'
    ]


def filter_zero_risk(
    vulnerabilities: List[VulnerabilityType],
) -> List[VulnerabilityType]:
    vulnerabilities = filter_non_confirmed_zero_risk_vuln(vulnerabilities)
    vulnerabilities = filter_non_requested_zero_risk_vuln(vulnerabilities)
    return vulnerabilities


async def get(vuln_id: str) -> Dict[str, FindingType]:
    vuln = await vulns_dal.get(vuln_id)
    if not vuln:
        raise VulnNotFound()
    first_vuln = cast(
        Dict[str, List[Dict[str, str]]],
        vuln[0]
    )
    if first_vuln.get(
        'historic_state', [{}]
    )[-1].get('state', '') == 'DELETED':
        raise VulnNotFound()
    return vuln[0]


async def get_by_finding(
    finding_id: str,
    vuln_id: str
) -> Dict[str, FindingType]:
    vuln = await vulns_dal.get_by_finding(finding_id, uuid=vuln_id)
    first_vuln = cast(
        Dict[str, List[Dict[str, str]]],
        vuln[0]
    )
    if not vuln:
        raise VulnNotFound()
    if first_vuln.get(
        'historic_state', [{}]
    )[-1].get('state', '') == 'DELETED':
        raise VulnNotFound()
    return vuln[0]


async def get_by_finding_and_uuids(
    finding_id: str,
    vuln_ids: Set[str],
) -> List[Dict[str, FindingType]]:
    finding_vulns = await vulns_dal.get_by_finding(finding_id)
    fin_vulns = [vuln for vuln in finding_vulns if vuln['UUID'] in vuln_ids]
    if len(fin_vulns) != len(vuln_ids):
        raise VulnNotInFinding()

    vulns = [
        vuln
        for vuln in fin_vulns
        if vulns_utils.filter_deleted_status(vuln)
    ]
    if len(vulns) != len(vuln_ids):
        raise VulnNotFound()
    return vulns


async def get_by_ids(vulns_ids: List[str]) -> List[Dict[str, FindingType]]:
    result: List[Dict[str, FindingType]] = await collect(
        get(vuln_id)
        for vuln_id in vulns_ids
    )
    return result


async def get_open_vuln_by_type(
    context: Any,
    finding_id: str,
) -> Dict[str, Union[int, List[Dict[str, str]]]]:
    """Get open vulnerabilities group by type."""
    finding_vulns_loader = context.finding_vulns_nzr
    vulnerabilities = await finding_vulns_loader.load(finding_id)
    finding: Dict[str, Union[int, List[Dict[str, str]]]] = {
        'openVulnerabilities': 0,
        'closedVulnerabilities': 0,
        'portsVulns': [],
        'linesVulns': [],
        'inputsVulns': []
    }
    vulns_types = ['ports', 'lines', 'inputs']
    for vuln in vulnerabilities:
        current_state = vulns_utils.get_last_status(vuln)
        if current_state == 'open':
            finding['openVulnerabilities'] = cast(
                int,
                finding['openVulnerabilities']
            ) + 1
            if vuln.get('vuln_type') in vulns_types:
                cast(
                    List[Dict[str, str]],
                    finding[f'{vuln.get("vuln_type", "")}Vulns']
                ).append({
                    'where': vuln.get('where'),
                    'specific': vuln.get('specific')
                })
            else:
                LOGGER.error(
                    'Vulnerability does not have the right type',
                    extra={
                        'extra': {
                            'vuln_uuid': vuln.get("UUID"),
                            'finding_id': finding_id
                        }
                    })
        elif current_state == 'closed':
            finding['closedVulnerabilities'] = cast(
                int,
                finding['closedVulnerabilities']
            ) + 1
        else:
            LOGGER.error(
                'Error: Vulnerability does not have the right state',
                extra={
                    'extra': {
                        'vuln_uuid': vuln['UUID'],
                        'finding_id': finding_id
                    }
                }
            )
    return finding


async def get_vulnerabilities_async(
    finding_id: str,
    table: aioboto3.session.Session.client,
    should_list_deleted: bool = False
) -> List[Dict[str, FindingType]]:
    vulnerabilities = await vulns_dal.get_vulnerabilities_async(
        finding_id,
        table,
        should_list_deleted
    )
    return [vulns_utils.format_data(vuln) for vuln in vulnerabilities]


async def get_vulnerabilities_by_type(
    context: Any,
    finding_id: str
) -> Dict[str, List[FindingType]]:
    """Get vulnerabilities group by type."""
    finding_vulns_loader = context.finding_vulns_nzr
    vulnerabilities = await finding_vulns_loader.load(finding_id)
    vulnerabilities_grouped = cast(
        List[Dict[str, FindingType]],
        await in_process(group_vulnerabilities, vulnerabilities)
    )
    vulnerabilities_formatted = vulns_utils.format_vulnerabilities(
        vulnerabilities_grouped
    )
    return vulnerabilities_formatted


async def get_vulnerabilities_file(
    context: Any,
    finding_id: str,
    project_name: str
) -> str:
    vulnerabilities = await get_vulnerabilities_by_type(context, finding_id)
    file_name = f'/tmp/{project_name}-{finding_id}_{str(uuid.uuid4())}.yaml'
    with open(file_name, 'w') as stream:
        yaml.safe_dump(vulnerabilities, stream, default_flow_style=False)

    uploaded_file_url = ''
    with open(file_name, 'rb') as bstream:
        uploaded_file = UploadFile(
            filename=bstream.name,
            content_type='application/yaml'
        )
        await uploaded_file.write(bstream.read())
        await uploaded_file.seek(0)
        uploaded_file_name = await vulns_dal.upload_file(uploaded_file)
        uploaded_file_url = await vulns_dal.sign_url(uploaded_file_name)
    return uploaded_file_url


def group_vulnerabilities(
    vulnerabilities: List[Dict[str, FindingType]]
) -> List[FindingType]:
    """Group vulnerabilities by specific field."""
    vuln_types = ['lines', 'ports', 'inputs']
    vuln_states = ['open', 'closed']
    total_vulnerabilities: Dict[str, Dict[str, FindingType]] = {}
    result_vulns: List[FindingType] = []
    for vuln_type in vuln_types:
        total_vulnerabilities[vuln_type] = {}
        for vuln_state in vuln_states:
            total_vulnerabilities[vuln_type][vuln_state] = []

    for vuln in vulnerabilities:
        all_states = cast(
            List[Dict[str, FindingType]],
            vuln.get('historic_state', [{}])
        )
        current_state = str(all_states[-1].get('state', ''))
        vuln_type = str(vuln.get('vuln_type', ''))
        cast(
            List[Dict[str, FindingType]],
            total_vulnerabilities[vuln_type][current_state]
        ).append(vuln)

    for vuln_type in vuln_types:
        for vuln_state in vuln_states:
            vulns_grouped = cast(
                Iterable[FindingType],
                vulns_utils.group_specific(
                    cast(
                        List[str],
                        total_vulnerabilities[vuln_type][vuln_state]
                    ),
                    vuln_type
                )
            )
            result_vulns.extend(vulns_grouped)
    return result_vulns


async def list_vulnerabilities_async(
    finding_ids: List[str],
    should_list_deleted: bool = False,
    include_requested_zero_risk: bool = False,
    include_confirmed_zero_risk: bool = False
) -> List[Dict[str, FindingType]]:
    """Retrieves all vulnerabilities for the requested findings"""
    vulns: List[Dict[str, FindingType]] = []
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(vulns_dal.TABLE_NAME)
        vulns = await collect(
            get_vulnerabilities_async(
                finding_id,
                table,
                should_list_deleted
            )
            for finding_id in finding_ids
        )

    result: List[Dict[str, FindingType]] = []
    for result_list in vulns:
        result.extend(
            cast(
                Iterable[Dict[str, FindingType]],
                result_list
            )
        )
    if not include_requested_zero_risk:
        result = vulns_utils.filter_non_requested_zero_risk(result)
    if not include_confirmed_zero_risk:
        result = vulns_utils.filter_non_confirmed_zero_risk(result)
    return result


async def mask_vuln(finding_id: str, vuln_id: str) -> bool:
    success = await vulns_dal.update(
        finding_id,
        vuln_id,
        {
            'specific': 'Masked',
            'where': 'Masked',
            'treatment_manager': 'Masked',
            'treatment_justification': 'Masked',
        }
    )
    return success


async def reject_zero_risk_vulnerabilities(
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    vuln_ids: List[str]
) -> bool:
    validate_justificaiton_length(justification)
    vulnerabilities = await get_by_finding_and_uuids(finding_id, set(vuln_ids))
    vulnerabilities = [
        validate_requested_zero_risk_vuln(vuln)
        for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = int(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_email: str = user_info['user_email']
    comment_data = {
        'comment_type': 'zero_risk',
        'content': justification,
        'parent': 0,
        'user_id': comment_id
    }
    create_comment = await comments_domain.create(
        int(finding_id),
        comment_data,
        user_info
    )
    reject_zero_risk_vulns = await collect(
        [
            vulns_dal.reject_zero_risk_vulnerability(
                user_email,
                today,
                comment_id,
                vuln
            )
            for vuln in vulnerabilities
        ]
    )
    success = all(reject_zero_risk_vulns) and create_comment[1]
    if not success:
        LOGGER.error('An error occurred rejecting zero risk vuln', **NOEXTRA)
    return success


async def request_verification(vulnerability: Dict[str, FindingType]) -> bool:
    return await vulns_dal.request_verification(vulnerability)


async def request_zero_risk_vulnerabilities(
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    vuln_ids: List[str]
) -> bool:
    validate_justificaiton_length(justification)
    vulnerabilities = await get_by_finding_and_uuids(finding_id, set(vuln_ids))
    vulnerabilities = [
        validate_not_requested_zero_risk_vuln(vuln)
        for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = int(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    comment_data = {
        'comment_type': 'zero_risk',
        'content': justification,
        'parent': 0,
        'user_id': comment_id
    }
    create_comment = await comments_domain.create(
        int(finding_id),
        comment_data,
        user_info
    )
    request_zero_risk_vulns = await collect(
        [
            vulns_dal.request_zero_risk_vulnerability(
                user_email,
                today,
                comment_id,
                vuln
            )
            for vuln in vulnerabilities
        ]
    )
    success = all(request_zero_risk_vulns) and create_comment[1]
    if success:
        await notifications_domain.request_zero_risk_vuln(
            info=info,
            finding_id=finding_id,
            justification=justification,
            requester_email=user_email,
        )
    else:
        LOGGER.error('An error occurred requesting zero risk vuln', **NOEXTRA)
    return success


async def send_finding_verified_email(  # pylint: disable=too-many-arguments
    context: Any,
    finding_id: str,
    finding_name: str,
    group_name: str,
    historic_verification: List[Dict[str, str]],
    vulnerabilities: List[str]
) -> None:
    group_loader = context.group_all
    organization_loader = context.organization
    group = await group_loader.load(group_name)
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']
    all_recipients = await group_access_domain.get_users_to_notify(group_name)
    recipients = await in_process(
        vulns_utils.get_reattack_requesters,
        historic_verification,
        vulnerabilities
    )
    recipients = [
        recipient for recipient in recipients if recipient in all_recipients
    ]
    schedule(
        mailer.send_mail_verified_finding(
            recipients,
            {
                'project': group_name,
                'organization': org_name,
                'finding_name': finding_name,
                'finding_url': (
                    f'{BASE_URL}/orgs/{org_name}/groups/{group_name}'
                    f'/vulns/{finding_id}/tracking'
                ),
                'finding_id': finding_id
            }
        )
    )


async def send_updated_treatment_mail(
    context: Any,
    treatment: str,
    finding: Dict[str, FindingType],
    vulnerabilities: str
) -> None:
    group_loader = context.group_all
    organization_loader = context.organization
    finding_id = str(finding['finding_id'])
    group_name = str(finding['project_name'])

    group = await group_loader.load(group_name)
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']
    managers = await group_access_domain.get_managers(group_name)

    schedule(
        mailer.send_mail_updated_treatment(
            managers,
            {
                'project': group_name,
                'treatment': treatment,
                'finding': str(finding.get('title')),
                'vulnerabilities': vulnerabilities,
                'finding_link':
                    f'{BASE_URL}/orgs/{org_name}/groups/{group_name}'
                    f'/vulns/{finding_id}'
            }
        )
    )


def set_updated_manager_mail_content(
    vulnerabilities: Dict[str, List[Dict[str, str]]]
) -> str:
    mail_content = ''
    for vuln_type in ['ports', 'lines', 'inputs']:
        type_vulns = vulnerabilities.get(vuln_type)
        if type_vulns:
            mail_content += '<br />'.join([
                f'- {list(vuln.values())[0]} ({list(vuln.values())[1]})'
                for vuln in type_vulns
            ])
            mail_content += '<br />'
    return mail_content


async def should_send_update_treatment(
    *,
    context: Any,
    finding_id: str,
    updated_vulns: List[Dict[str, FindingType]],
    treatment: str,
) -> None:
    translations = {
        'IN PROGRESS': 'In Progress',
    }
    if treatment in translations:
        finding_loader = context.loaders.finding
        finding = await finding_loader.load(finding_id)
        vulns_grouped = group_vulnerabilities(updated_vulns)
        vulns_data = vulns_utils.format_vulnerabilities(
            cast(List[Dict[str, FindingType]], vulns_grouped)
        )
        mail_content = set_updated_manager_mail_content(
            cast(Dict[str, List[Dict[str, str]]], vulns_data)
        )
        await send_updated_treatment_mail(
            context,
            translations[treatment],
            finding,
            mail_content
        )


async def update_historic_state_dates(
    finding_id: str,
    vuln: Dict[str, FindingType],
    date: str
) -> bool:
    historic_state = cast(Historic, vuln['historic_state'])
    for state_info in historic_state:
        state_info['date'] = date
    success = await vulns_dal.update(
        finding_id,
        cast(str, vuln['UUID']),
        {'historic_state': historic_state}
    )
    return success


async def update_treatment_vuln(
    vuln_info: VulnerabilityType,
    finding_id: str,
    updated_values: Dict[str, FindingType],
    info: GraphQLResolveInfo,
) -> bool:
    success = True
    vulnerability = vuln_info['id']
    new_info = copy.copy(updated_values)
    if new_info.get('tag'):
        new_info['tag'] = cast(List[str], vuln_info['tags'])
        tags = str(updated_values['tag']).split(',')
        validations.validate_fields(tags)
        for tag in tags:
            if tag.strip():
                cast(List[str], new_info['tag']).append(tag.strip())
        new_info['tag'] = cast(
            List[str],
            list(
                set(
                    cast(
                        Iterable[Collection[str]],
                        new_info['tag']
                    )
                )
            )
        )
        new_info['tag'] = [
            html.unescape(tag)
            for tag in cast(List[str], new_info['tag'])
        ]
    new_info = {
        key: None if not value else value
        for key, value in new_info.items()
    }
    new_info = {
        util.camelcase_to_snakecase(k): new_info.get(k)
        for k in new_info
    }
    result_update_vuln = await vulns_dal.update(
        finding_id,
        str(vulnerability),
        new_info
    )
    if not result_update_vuln:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to update vulnerability: '
            f'{vulnerability} from finding:{finding_id}'
        )
        success = False
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Updated vulnerability: '
            f'{vulnerability} from finding: {finding_id} successfully'
        )
    return success


async def update_treatment_vulns(
    vulnerability_id: str,
    finding_id: str,
    updated_values: Dict[str, FindingType],
    info: GraphQLResolveInfo
) -> bool:
    del updated_values['finding_id']
    vuln_info = await info.context.loaders.vulnerability.load(vulnerability_id)
    success: bool = await update_treatment_vuln(
        cast(VulnerabilityType, vuln_info),
        finding_id,
        updated_values,
        info
    )
    return success


async def update_treatments(
    vulnerability_id: str,
    finding_id: str,
    updated_values: Dict[str, FindingType],
    info: GraphQLResolveInfo
) -> bool:
    updated_values.pop('vulnerabilities', None)
    if updated_values.get('tag') == '':
        updated_values.pop('tag', None)
    if cast(int, updated_values.get('severity', 0)) < 0:
        updated_values['severity'] = ''
    if 'external_bts' in updated_values:
        validations.validate_url(str(updated_values.get('external_bts', '')))
        validations.validate_field_length(
            str(updated_values.get('external_bts', '')),
            80
        )
    return await update_treatment_vulns(
        vulnerability_id,
        finding_id,
        updated_values,
        info
    )


async def update_vuln_state(
    info: GraphQLResolveInfo,
    vulnerability: Dict[str, FindingType],
    item: Dict[str, str],
    finding_id: str,
    current_day: str
) -> bool:
    """Update vulnerability state."""
    historic_state = cast(
        List[Dict[str, str]],
        vulnerability.get('historic_state')
    )
    last_state = historic_state[-1]
    data_to_update: Dict[str, FindingType] = {}
    if last_state.get('state') != item.get('state'):
        user_data = cast(UserType, await util.get_jwt_content(info.context))
        source = util.get_source(info.context)
        analyst = str(user_data['user_email'])
        current_state = {
            'analyst': analyst,
            'date': current_day,
            'source': source,
            'state': item.get('state', '')
        }
        historic_state.append(current_state)
        data_to_update['historic_state'] = historic_state

    if item['vuln_type'] == 'inputs':
        data_to_update['stream'] = item['stream']
    if item['vuln_type'] == 'lines':
        data_to_update['commit_hash'] = item['commit_hash']

    if data_to_update:
        return await vulns_dal.update(
            finding_id,
            str(vulnerability.get('UUID')),
            data_to_update
        )
    return True


def validate_justificaiton_length(justification: str) -> None:
    """ Validate justification length"""
    max_justification_length = 2000
    if len(justification) > max_justification_length:
        raise InvalidJustificationMaxLength(max_justification_length)


def validate_not_requested_zero_risk_vuln(
    vuln: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    """ Validate zero risk vuln is not already resquested """
    historic_zero_risk = cast(
        List[Dict[str, FindingType]],
        vuln.get('historic_zero_risk', [{}])
    )
    if historic_zero_risk[-1].get('status', '') == 'REQUESTED':
        raise AlreadyZeroRiskRequested()
    return vuln


def validate_requested_zero_risk_vuln(
    vuln: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    """ Validate zero risk vuln is already resquested """
    historic_zero_risk = cast(
        List[Dict[str, FindingType]],
        vuln.get('historic_zero_risk', [{}])
    )
    if historic_zero_risk[-1].get('status', '') != 'REQUESTED':
        raise NotZeroRiskRequested()
    return vuln


async def verify(
    *,
    context: Any,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerabilities: List[Dict[str, FindingType]],
    closed_vulns: List[str],
    date: str,
    vulns_to_close_from_file: List[Dict[str, str]]
) -> List[bool]:
    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    list_closed_vulns = sorted(
        [
            [
                vuln
                for vuln in vulnerabilities
                if vuln['UUID'] == closed_vuln
            ][0]
            for closed_vuln in closed_vulns
        ],
        key=itemgetter('UUID')
    )
    success: List[bool] = await collect(
        update_vuln_state(
            info,
            vuln_to_close,
            {
                'commit_hash': (
                    close_item['commit_hash']
                    if close_item and close_item['vuln_type'] == 'lines'
                    else ''
                ),
                'state': 'closed',
                'stream': (
                    close_item['stream']
                    if close_item and close_item['vuln_type'] == 'inputs'
                    else ''
                ),
                'vuln_type': close_item['vuln_type'] if close_item else '',
            },
            finding_id,
            date
        )
        for vuln_to_close, close_item in zip_longest(
            list_closed_vulns,
            vulns_to_close_from_file,
            fillvalue={}
        )
    )
    schedule(
        send_finding_verified_email(
            context,
            finding_id,
            str(finding.get('title', '')),
            str(finding.get('project_name', '')),
            cast(
                List[Dict[str, str]],
                finding.get('historic_verification', [])
            ),
            [str(vuln.get('UUID', '')) for vuln in vulnerabilities],
        )
    )
    return success


async def verify_vulnerability(
    vulnerability: Dict[str, FindingType]
) -> bool:
    return await vulns_dal.verify_vulnerability(vulnerability)
