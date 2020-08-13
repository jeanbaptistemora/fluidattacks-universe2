# pylint:disable=too-many-branches
import re
import random
from datetime import datetime
from decimal import Decimal
from typing import cast, Dict, List, Tuple, Any
import pytz
from django.conf import settings
from graphql.type.definition import GraphQLResolveInfo

from backend import util
from backend.dal import finding as finding_dal
from backend.domain import vulnerability as vuln_domain
from backend.exceptions import (
    AlreadyApproved,
    AlreadySubmitted,
    DraftWithoutVulns,
    IncompleteDraft,
    InvalidDraftTitle,
    NotSubmitted,
)
from backend.typing import (
    User as UserType
)
from backend.utils import (
    findings as finding_utils
)
from .finding import get_finding


async def reject_draft(draft_id: str, reviewer_email: str) -> bool:
    draft_data = await get_finding(draft_id)
    history = cast(
        List[Dict[str, str]],
        draft_data.get('historicState', [{}])
    )
    status = history[-1].get('state')
    success = False

    if 'releaseDate' not in draft_data:
        if status == 'SUBMITTED':
            tzn = pytz.timezone(settings.TIME_ZONE)
            today = datetime.now(tz=tzn).today()
            rejection_date = str(today.strftime('%Y-%m-%d %H:%M:%S'))
            history.append({
                'date': rejection_date,
                'analyst': reviewer_email,
                'state': 'REJECTED'
            })

            success = await finding_dal.update(draft_id, {
                'release_date': None,
                'historic_state': history
            })
            if success:
                await finding_utils.send_draft_reject_mail(
                    draft_id,
                    str(draft_data.get('projectName', '')),
                    str(draft_data.get('analyst', '')),
                    str(draft_data.get('finding', '')),
                    reviewer_email
                )
        else:
            raise NotSubmitted()
    else:
        raise AlreadyApproved()

    return success


async def approve_draft(
        draft_id: str,
        reviewer_email: str) -> Tuple[bool, str]:
    draft_data = await get_finding(draft_id)
    submission_history = cast(
        List[Dict[str, str]],
        draft_data.get('historicState')
    )
    release_date: str = ''
    success = False

    if ('releaseDate' not in draft_data and
            submission_history[-1].get('state') != 'DELETED'):
        vulns = await vuln_domain.list_vulnerabilities_async([draft_id])
        has_vulns = [
            vuln for vuln in vulns
            if vuln_domain.filter_deleted_status(vuln)
        ]
        if has_vulns:
            if 'reportDate' in draft_data:
                tzn = pytz.timezone(settings.TIME_ZONE)
                today = datetime.now(tz=tzn).today()
                release_date = str(today.strftime('%Y-%m-%d %H:%M:%S'))
                history = cast(
                    List[Dict[str, str]],
                    draft_data.get('historicState', [{}])
                )
                history.append({
                    'date': release_date,
                    'analyst': reviewer_email,
                    'state': 'APPROVED'
                })
                success = await finding_dal.update(draft_id, {
                    'lastVulnerability': release_date,
                    'releaseDate': release_date,
                    'treatment': 'NEW',
                    'historic_state': history
                })
            else:
                raise NotSubmitted()
        else:
            raise DraftWithoutVulns()
    else:
        raise AlreadyApproved()

    return success, release_date


async def create_draft(
        info: GraphQLResolveInfo,
        project_name: str,
        title: str,
        **kwargs: Any) -> bool:
    last_fs_id = 550000000
    finding_id = str(random.randint(last_fs_id, 1000000000))
    tzn = pytz.timezone(settings.TIME_ZONE)
    project_name = project_name.lower()
    today = datetime.now(tz=tzn).today()
    creation_date = today.strftime('%Y-%m-%d %H:%M:%S')
    user_data = cast(UserType, util.get_jwt_content(info.context))
    analyst_email = str(user_data.get('user_email', ''))
    submission_history = {
        'analyst': analyst_email,
        'date': creation_date,
        'state': 'CREATED'
    }
    if util.is_api_token(user_data):
        submission_history.update({
            'analyst': f'api-{analyst_email}',
            'origin': kwargs.get('origin', 'api')})

    if 'description' in kwargs:
        kwargs['vulnerability'] = kwargs['description']
        del kwargs['description']
    if 'recommendation' in kwargs:
        kwargs['effect_solution'] = kwargs['recommendation']
        del kwargs['recommendation']
    if 'type' in kwargs:
        kwargs['finding_type'] = kwargs['type']
        del kwargs['type']

    finding_attrs = kwargs.copy()
    finding_attrs.update({
        'analyst': analyst_email,
        'cvss_version': '3.1',
        'exploitability': 0,
        'files': [],
        'finding': title,
        'report_date': creation_date,
        'historic_state': [submission_history],
        'historic_treatment': [{
            'treatment': 'NEW',
            'date': creation_date,
            'user': analyst_email
        }]
    })

    if re.search(r'^[A-Z]+\.(H\.|S\.|SH\.)??[0-9]+\. .+', title):

        return await finding_dal.create(
            finding_id, project_name, finding_attrs)
    raise InvalidDraftTitle()


async def submit_draft(finding_id: str, analyst_email: str) -> bool:
    success = False
    finding = await get_finding(finding_id)
    submission_history = cast(
        List[Dict[str, str]],
        finding.get('historicState')
    )

    if ('releaseDate' not in finding and
            submission_history[-1].get('state') != 'DELETED'):
        is_submitted = submission_history[-1].get('state') == 'SUBMITTED'
        if not is_submitted:
            finding_evidence = cast(
                Dict[str, Dict[str, str]],
                finding['evidence']
            )
            evidence_list = cast(
                List[Dict[str, Dict[str, str]]],
                [
                    finding_evidence.get(ev_name)
                    for ev_name in finding_evidence
                ]
            )
            has_evidence = any([
                str(evidence.get('url', ''))
                for evidence in evidence_list
            ])
            has_severity = float(str(finding['severityCvss'])) > Decimal(0)
            has_vulns = await vuln_domain.list_vulnerabilities_async(
                [finding_id]
            )

            if all([has_evidence, has_severity, has_vulns]):
                today = datetime.now(
                    tz=pytz.timezone(settings.TIME_ZONE)
                ).today()
                report_date = today.strftime('%Y-%m-%d %H:%M:%S')
                history = cast(
                    List[Dict[str, str]],
                    finding.get('historicState', [])
                )
                history.append({
                    'analyst': analyst_email,
                    'date': report_date,
                    'state': 'SUBMITTED'
                })

                success = await finding_dal.update(finding_id, {
                    'report_date': report_date,
                    'historic_state': history
                })
                if success:
                    await finding_utils.send_new_draft_mail(
                        analyst_email,
                        finding_id,
                        str(finding.get('finding', '')),
                        str(finding.get('projectName', ''))
                    )
            else:
                required_fields = {
                    'evidence': has_evidence,
                    'severity': has_severity,
                    'vulnerabilities': has_vulns
                }
                raise IncompleteDraft([
                    field
                    for field in required_fields
                    if not required_fields[field]
                ])
        else:
            raise AlreadySubmitted()
    else:
        raise AlreadyApproved()

    return success
