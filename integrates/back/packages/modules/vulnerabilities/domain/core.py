"""Domain functions for vulnerabilities."""   # pylint:disable=too-many-lines

# Standard libraries
import copy
import html
import html.parser
import json
import logging
import logging.config
import os
import uuid
from contextlib import AsyncExitStack
from itertools import (
    chain,
    zip_longest,
)
from operator import itemgetter
from time import time
from typing import (
    Any,
    Awaitable,
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
from pykwalify.core import Core
from pykwalify.errors import (
    CoreError,
    SchemaError,
)
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
from backend.dal.helpers.dynamodb import start_context
from backend.domain import project as project_domain
from backend.exceptions import (
    AlreadyRequested,
    AlreadyZeroRiskRequested,
    InvalidFileSize,
    InvalidJustificationMaxLength,
    InvalidPath,
    InvalidPort,
    InvalidSchema,
    InvalidSpecific,
    InvalidVulnsNumber,
    NotVerificationRequested,
    NotZeroRiskRequested,
    VulnAlreadyClosed,
    VulnNotFound,
    VulnNotInFinding,
)
from backend.typing import (
    Finding as FindingType,
    Historic,
    User as UserType,
    Vulnerability as VulnerabilityType,
)
from comments import domain as comments_domain
from findings import dal as findings_dal
from newutils import (
    datetime as datetime_utils,
    findings as finding_utils,
    validations,
    vulnerabilities as vulns_utils,
)
from notifications import domain as notifications_domain
from roots import domain as roots_domain
from vulnerabilities import dal as vulns_dal
from __init__ import BASE_URL
from .utils import validate_stream


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _validate_roots(
    *,
    group_name: str,
    vulnerabilities: Dict[str, List[Dict[str, str]]]
) -> None:
    nicknames = set(
        vuln['repo_nickname']
        for vulns in vulnerabilities.values()
        for vuln in vulns
        if 'repo_nickname' in vuln
    )
    await collect(
        tuple(
            roots_domain.get_root_by_nickname(
                group_name=group_name,
                repo_nickname=nickname
            )
            for nickname in nicknames
        )
    )


async def add_vuln_to_dynamo(
    *,
    item: Dict[str, str],
    specific: str,
    finding_id: str,
    info: GraphQLResolveInfo,
    vulnerability: Optional[Dict[str, FindingType]]
) -> bool:
    """Add vulnerability to dynamo."""
    historic_state = []
    response = False
    current_day = datetime_utils.get_now_as_str()
    user_data = cast(UserType, await util.get_jwt_content(info.context))
    email = str(user_data['user_email'])
    if vulnerability:
        return await update_vuln_state(
            info,
            vulnerability,
            item,
            finding_id,
            current_day
        )

    data: Dict[str, FindingType] = {'repo_nickname': item['repo_nickname']}
    source = util.get_source(info.context)
    new_state: Dict[str, str] = {
        'analyst': email,
        'date': current_day,
        'source': source
    }
    data['historic_treatment'] = [{
        'date': current_day,
        'treatment': 'NEW'
    }]
    data['vuln_type'] = item.get('vuln_type', '')
    data['where'] = item.get('where', '')
    data['specific'] = specific
    data['finding_id'] = finding_id
    if 'stream' in item:
        data['stream'] = item['stream']
    if 'commit_hash' in item:
        data['commit_hash'] = item['commit_hash']
    data['UUID'] = str(uuid.uuid4())
    if item.get('state'):
        new_state['state'] = item['state']
        historic_state.append(new_state)
        data['historic_state'] = historic_state
        response = await vulns_dal.create(data)
    else:
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to add vulnerability without state'
        )
    return response


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


def get_last_approved_state(vuln: Dict[str, FindingType]) -> Dict[str, str]:
    historic_state = cast(Historic, vuln.get('historic_state', [{}]))
    return historic_state[-1]


def get_last_status(vuln: Dict[str, FindingType]) -> str:
    historic_state = cast(Historic, vuln.get('historic_state', [{}]))
    return historic_state[-1].get('state', '')


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
        current_state = get_last_status(vuln)
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


async def get_vulns_to_add(
    vulnerabilities: Dict[str, List[VulnerabilityType]],
) -> List[Dict[str, str]]:
    coroutines = []
    for vuln_type in ['inputs', 'lines', 'ports']:
        file_vuln = vulnerabilities.get(vuln_type)
        if file_vuln:
            coroutines.extend([
                map_vulnerability_type(vuln, vuln_type)
                for vuln in file_vuln
            ])
        else:
            pass
            # If a file does not have a type of vulnerabilities,
            # this does not represent an error or an exceptional condition.
    return list(chain.from_iterable(await collect(coroutines)))


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


def is_accepted_undefined_vulnerability(
    vulnerability: Dict[str, FindingType]
) -> bool:
    historic_treatment = cast(Historic, vulnerability['historic_treatment'])
    return (
        historic_treatment[-1]['treatment'] == 'ACCEPTED_UNDEFINED' and
        get_last_status(vulnerability) == 'open'
    )


def is_reattack_requested(vuln: Dict[str, FindingType]) -> bool:
    response = False
    historic_verification = vuln.get('historic_verification', [{}])
    if cast(
        List[Dict[str, str]],
        historic_verification
    )[-1].get('status', '') == 'REQUESTED':
        response = True
    return response


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


async def map_vulnerability_type(
    item: VulnerabilityType,
    vuln_type: str,
) -> List[Dict[str, str]]:
    """Add vulnerability to dynamo."""
    response = []
    where_headers = {
        'inputs': {'where': 'url', 'specific': 'field'},
        'lines': {'where': 'path', 'specific': 'line'},
        'ports': {'where': 'host', 'specific': 'port'}
    }

    data: Dict[str, str] = {
        'repo_nickname': item.get('repo_nickname'),
        'state': str(item.get('state', '')),
        'vuln_type': vuln_type
    }
    data['where'] = str(item.get(where_headers[vuln_type]['where']))
    specific = str(item.get(where_headers[vuln_type]['specific']))

    if vuln_type == 'lines' and data['where'].find('\\') >= 0:
        path = data['where'].replace('\\', '\\\\')
        raise InvalidPath(expr=f'"values": "{path}"')
    if 'stream' in item:
        validate_stream(data['where'], str(item['stream']))
        data['stream'] = str(item['stream'])
    if 'commit_hash' in item:
        data['commit_hash'] = str(item['commit_hash'])
    if vulns_utils.is_range(specific) or vulns_utils.is_sequence(specific):
        response.extend(
            ungroup_vulnerability_specific(vuln_type, specific, data)
        )
    else:
        if vuln_type == 'ports' and not 0 <= int(specific) <= 65535:
            raise InvalidPort(expr=f'"values": "{specific}"')
        response.append({**data, 'specific': specific})
    return response


async def map_vulns_to_dynamo(
    info: GraphQLResolveInfo,
    vulnerabilities: Dict[str, List[VulnerabilityType]],
    finding: Dict[str, FindingType]
) -> bool:
    """Map vulnerabilities and send it to dynamo."""
    coroutines: List[Awaitable[bool]] = []
    finding_id = finding.get('finding_id', '')
    vulns_to_add = await get_vulns_to_add(vulnerabilities)
    if len(vulns_to_add) > 100:
        raise InvalidVulnsNumber()

    finding_vulns = await vulns_dal.get_by_finding(str(finding_id))
    vulns: List[Dict[str, FindingType]] = [
        next(
            iter([
                vuln
                for vuln in finding_vulns
                if (
                    vuln_to_add.get('vuln_type', '') ==
                    vuln.get('vuln_type', '_') and
                    vuln_to_add.get('where', '') == vuln.get('where', '_') and
                    vuln_to_add.get('specific', '') ==
                    vuln.get('specific', '_')
                )
            ]),
            {}
        )
        for vuln_to_add in vulns_to_add
    ]

    closed_vulns_to_reattack: List[Dict[str, str]] = sorted(
        [
            {
                **vuln_to_add,
                'UUID': str(vuln['UUID'])
            }
            for vuln, vuln_to_add in zip(vulns, vulns_to_add)
            if (
                is_reattack_requested(vuln) and
                get_last_status(vuln) == 'open' and
                vuln_to_add.get('state') == 'closed'
            )
        ],
        key=itemgetter('UUID')
    )
    closed_vulns_uuids = {vuln['UUID'] for vuln in closed_vulns_to_reattack}

    coroutines.extend([
        add_vuln_to_dynamo(
            item=vuln_to_add,
            specific=str(vuln_to_add.get('specific')),
            finding_id=str(finding_id),
            info=info,
            vulnerability=vuln,
        )
        for vuln_to_add, vuln in zip(vulns_to_add, vulns)
        if str(vuln.get('UUID', '')) not in closed_vulns_uuids
    ])
    if closed_vulns_to_reattack:
        user_data = cast(UserType, await util.get_jwt_content(info.context))
        coroutines.append(
            verify_vulnerabilities(
                info=info,
                finding_id=str(finding_id),
                user_info=user_data,
                parameters={
                    'justification': 'The vulnerability was verified'
                                     ' by closing it',
                    'closed_vulns': list(closed_vulns_uuids),
                },
                vulns_to_close_from_file=closed_vulns_to_reattack,
            )
        )
    return all(await collect(coroutines))


async def process_file(
    info: GraphQLResolveInfo,
    file_input: UploadFile,
    finding: Dict[str, FindingType]
) -> bool:
    """Process a file."""
    success = False
    finding_id = finding.get('finding_id', '')
    group_name: str = finding['project_name']
    raw_content = await file_input.read()
    raw_content = cast(bytes, raw_content).decode()
    file_content = html.escape(raw_content, quote=False)
    await file_input.seek(0)
    vulnerabilities = yaml.safe_load(file_content)
    file_url = f'/tmp/vulnerabilities-{uuid.uuid4()}-{finding_id}.yaml'
    with open(file_url, 'w') as stream:
        yaml.safe_dump(vulnerabilities, stream)
    if validate_file_schema(file_url, info):
        await _validate_roots(
            group_name=group_name,
            vulnerabilities=vulnerabilities
        )
        success = await map_vulns_to_dynamo(info, vulnerabilities, finding)
    else:
        success = False
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


async def request_verification(  # pylint: disable=too-many-arguments
    context: Any,
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    vuln_ids: List[str]
) -> bool:
    finding = await findings_dal.get_finding(finding_id)
    vulnerabilities = await get_by_finding_and_uuids(finding_id, set(vuln_ids))
    vulnerabilities = [
        validate_requested_verification(vuln)
        for vuln in vulnerabilities
    ]
    vulnerabilities = [validate_closed(vuln) for vuln in vulnerabilities]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = int(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_email: str = user_info['user_email']
    historic_verification = cast(
        List[Dict[str, Union[str, int, List[str]]]],
        finding.get('historic_verification', [])
    )
    historic_verification.append({
        'comment': comment_id,
        'date': today,
        'status': 'REQUESTED',
        'user': user_email,
        'vulns': vuln_ids
    })
    update_finding = await findings_dal.update(
        finding_id,
        {'historic_verification': historic_verification}
    )
    comment_data = {
        'comment_type': 'verification',
        'content': justification,
        'parent': 0,
        'user_id': comment_id
    }
    await comments_domain.create(int(finding_id), comment_data, user_info)

    update_vulns = await collect(
        map(vulns_dal.request_verification, vulnerabilities)
    )
    if all(update_vulns) and update_finding:
        schedule(
            finding_utils.send_remediation_email(
                context,
                user_email,
                finding_id,
                str(finding.get('finding', '')),
                str(finding.get('project_name', '')),
                justification
            )
        )
    else:
        LOGGER.error('An error occurred remediating', **NOEXTRA)
    return all(update_vulns)


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
    managers = await project_domain.get_managers(group_name)

    schedule(
        mailer.send_mail_updated_treatment(
            managers,
            {
                'project': group_name,
                'treatment': treatment,
                'finding': str(finding.get('finding')),
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
        'ACCEPTED_UNDEFINED_APPROVED': 'Eternally accepted',
        'ACCEPTED_UNDEFINED_SUBMITTED': (
            'Eternally accepted (Pending approval)'
        ),
        'ACCEPTED': 'Temporarily Accepted',
        'IN PROGRESS': 'In Progress',
    }
    if treatment in translations:
        finding = await findings_dal.get_finding(finding_id)
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


def ungroup_vulnerability_specific(
    vuln: str,
    specific: str,
    data: Dict[str, str]
) -> List[Dict[str, str]]:
    """Add vulnerability auxiliar."""
    if vuln in ('lines', 'ports'):
        specific_values = vulns_utils.ungroup_specific(specific)
    else:
        specific_values = [
            spec
            for spec in specific.split(',')
            if spec
        ]
    if (
        vuln == 'ports' and not
        all((0 <= int(i) <= 65535) for i in specific_values)
    ):
        error_value = f'"values": "{specific}"'
        raise InvalidPort(expr=error_value)
    if not specific_values:
        raise InvalidSpecific()
    return [
        {
            **data,
            'specific': specific
        }
        for specific in specific_values
    ]


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


async def upload_file(
    info: GraphQLResolveInfo,
    file_input: UploadFile,
    finding: Dict[str, FindingType]
) -> bool:
    mib = 1048576
    success = False
    if await util.get_file_size(file_input) < 1 * mib:
        success = await process_file(info, file_input, finding)
    else:
        raise InvalidFileSize()
    return success


def validate_closed(vuln: Dict[str, FindingType]) -> Dict[str, FindingType]:
    """ Validate vuln closed """
    if cast(
        List[Dict[str, FindingType]],
        vuln.get('historic_state', [{}])
    )[-1].get('state') == 'closed':
        raise VulnAlreadyClosed()
    return vuln


def validate_file_schema(file_url: str, info: GraphQLResolveInfo) -> bool:
    """Validate if a file has the correct schema."""
    schema_dir = os.path.dirname(os.path.abspath(__file__))
    schema_dir = os.path.join(schema_dir, 'vuln_template.yaml')
    core = Core(source_file=file_url, schema_files=[schema_dir])
    is_valid = False
    try:
        core.validate(raise_exception=True)
        is_valid = True
    except SchemaError:
        lines_of_exceptions = core.errors
        errors_values = [
            getattr(x, 'pattern', '')
            for x in lines_of_exceptions
            if not hasattr(x, 'key')
        ]
        errors_keys = [
            x
            for x in lines_of_exceptions
            if hasattr(x, 'key')
        ]
        errors_values_formated = [json.dumps(x) for x in errors_values]
        errors_keys_formated = [
            f'"{x.key}"'
            for x in errors_keys
        ]
        errors_keys_joined = ','.join(errors_keys_formated)
        errors_values_joined = ','.join(errors_values_formated)
        error_value = (
            f'"values": [{errors_values_joined}], '
            f'"keys": [{errors_keys_joined}]'
        )
        util.cloudwatch_log(
            info.context,
            'Error: An error occurred validating vulnerabilities file'
        )
        raise InvalidSchema(expr=error_value)
    except CoreError:
        raise InvalidSchema()
    finally:
        os.unlink(file_url)
    return is_valid


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


def validate_requested_verification(
    vuln: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    """ Validate vuln is not resquested """
    historic_verification = cast(
        List[Dict[str, FindingType]],
        vuln.get('historic_verification', [{}])
    )
    if historic_verification[-1].get('status', '') == 'REQUESTED':
        raise AlreadyRequested()
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


def validate_verify(vuln: Dict[str, FindingType]) -> Dict[str, FindingType]:
    """ Validate vuln is resquested """
    if not is_reattack_requested(vuln):
        raise NotVerificationRequested()
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
    finding = await findings_dal.get_finding(finding_id)
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
        finding_utils.send_finding_verified_email(
            context,
            finding_id,
            str(finding.get('finding', '')),
            str(finding.get('project_name', '')),
            cast(
                List[Dict[str, str]],
                finding.get('historic_verification', [])
            ),
            [str(vuln.get('UUID', '')) for vuln in vulnerabilities],
        )
    )
    return success


async def verify_vulnerabilities(  # pylint: disable=too-many-locals
    *,
    info: GraphQLResolveInfo,
    finding_id: str,
    user_info: Dict[str, str],
    parameters: Dict[str, FindingType],
    vulns_to_close_from_file: List[Dict[str, str]]
) -> bool:
    finding_vulns_loader = info.context.loaders.finding_vulns_all
    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    vuln_ids = (
        cast(List[str], parameters.get('open_vulns', [])) +
        cast(List[str], parameters.get('closed_vulns', []))
    )
    vulnerabilities = [
        vuln
        for vuln in await finding_vulns_loader.load(finding_id)
        if vuln['id'] in vuln_ids
    ]
    vulnerabilities = [validate_verify(vuln) for vuln in vulnerabilities]
    vulnerabilities = [validate_closed(vuln) for vuln in vulnerabilities]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = int(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_email: str = user_info['user_email']
    historic_verification = cast(
        List[Dict[str, Union[str, int, List[str]]]],
        finding.get('historic_verification', [])
    )
    historic_verification.append({
        'comment': comment_id,
        'date': today,
        'status': 'VERIFIED',
        'user': user_email,
        'vulns': vuln_ids
    })
    update_finding = await findings_dal.update(
        finding_id,
        {'historic_verification': historic_verification}
    )
    comment_data = {
        'comment_type': 'verification',
        'content': parameters.get('justification', ''),
        'parent': 0,
        'user_id': comment_id
    }
    await comments_domain.create(int(finding_id), comment_data, user_info)

    success = await collect(
        map(vulns_dal.verify_vulnerability, vulnerabilities)
    )
    if all(success) and update_finding:
        success = await verify(
            context=info.context.loaders,
            info=info,
            finding_id=finding_id,
            vulnerabilities=vulnerabilities,
            closed_vulns=cast(List[str], parameters.get('closed_vulns', [])),
            date=today,
            vulns_to_close_from_file=vulns_to_close_from_file
        )
    else:
        LOGGER.error('An error occurred verifying', **NOEXTRA)
    return all(success)
