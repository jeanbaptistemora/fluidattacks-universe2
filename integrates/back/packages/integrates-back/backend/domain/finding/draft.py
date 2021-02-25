# pylint:disable=too-many-branches
import re
import random
from decimal import Decimal
from typing import cast, Dict, List, Tuple, Any, Set

from aioextensions import (
    collect,
)
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
from backend.filters import (
    finding as finding_filters,
)
from backend.typing import (
    Finding as FindingType,
    User as UserType
)
from backend.utils import (
    datetime as datetime_utils,
    findings as finding_utils,
)


async def reject_draft(
    context: Any,
    draft_id: str,
    reviewer_email: str
) -> bool:
    finding_loader = context.loaders.finding
    draft_data = await finding_loader.load(draft_id)
    history = cast(
        List[Dict[str, str]],
        draft_data['historic_state']
    )
    success = False
    is_finding_approved = finding_filters.is_approved(draft_data)
    is_finding_deleted = finding_filters.is_deleted(draft_data)
    is_finding_submitted = finding_filters.is_submitted(draft_data)

    if (not is_finding_approved and not is_finding_deleted):
        if is_finding_submitted:
            rejection_date = datetime_utils.get_as_str(
                datetime_utils.get_now()
            )
            source = util.get_source(context)
            history.append({
                'date': rejection_date,
                'analyst': reviewer_email,
                'source': source,
                'state': 'REJECTED'
            })

            success = await finding_dal.update(draft_id, {
                'historic_state': history
            })
        else:
            raise NotSubmitted()
    else:
        raise AlreadyApproved()

    return success


async def approve_draft(
    context: Any,
    draft_id: str,
    reviewer_email: str
) -> Tuple[bool, str]:
    finding_all_vulns_loader = context.loaders.finding_vulns_all
    finding_vulns_loader = context.loaders.finding_vulns_nzr
    finding_loader = context.loaders.finding
    draft_data = await finding_loader.load(draft_id)
    release_date: str = ''
    success = False

    if (
        not finding_filters.is_approved(draft_data) and
        not finding_filters.is_deleted(draft_data)
    ):
        vulns = await finding_vulns_loader.load(draft_id)
        has_vulns = [
            vuln for vuln in vulns
            if vuln_domain.filter_deleted_status(vuln)
        ]
        if has_vulns:
            if finding_filters.is_submitted(draft_data):
                release_date = datetime_utils.get_as_str(
                    datetime_utils.get_now()
                )
                history = cast(
                    List[Dict[str, str]],
                    draft_data['historic_state']
                )
                history.append({
                    'date': release_date,
                    'analyst': reviewer_email,
                    'source': util.get_source(context),
                    'state': 'APPROVED'
                })
                finding_update_success = await finding_dal.update(draft_id, {
                    'historic_state': history
                })
                all_vulns = await finding_all_vulns_loader.load(draft_id)
                vuln_update_success = await collect(
                    vuln_domain.update_historic_state_dates(
                        draft_id,
                        vuln,
                        release_date
                    )
                    for vuln in all_vulns
                )

                success = all(vuln_update_success) and finding_update_success
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
    **kwargs: Any
) -> bool:
    last_fs_id = 550000000
    finding_id = str(random.randint(last_fs_id, 1000000000))
    project_name = project_name.lower()
    creation_date = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
    user_data = cast(UserType, await util.get_jwt_content(info.context))
    analyst_email = str(user_data.get('user_email', ''))
    source = util.get_source(info.context)
    submission_history = {
        'analyst': analyst_email,
        'date': creation_date,
        'source': source,
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
        'historic_state': [submission_history],
    })

    if re.match(r'^F[0-9]{3}\. .+', title):

        return await finding_dal.create(
            finding_id, project_name, finding_attrs)
    raise InvalidDraftTitle()


async def submit_draft(  # pylint: disable=too-many-locals
    context: Any,
    finding_id: str,
    analyst_email: str
) -> bool:
    success = False
    finding_vulns_loader = context.finding_vulns
    finding_loader = context.finding
    finding = await finding_loader.load(finding_id)
    is_finding_approved = finding_filters.is_approved(finding)
    is_finding_deleted = finding_filters.is_deleted(finding)
    is_finding_submitted = finding_filters.is_submitted(finding)

    if (not is_finding_approved and not is_finding_deleted):
        if not is_finding_submitted:
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
            has_evidence = any([  # noqa
                str(evidence.get('url', ''))
                for evidence in evidence_list
            ])
            has_severity = float(str(finding['severity_score'])) > Decimal(0)
            has_vulns = await finding_vulns_loader.load(finding_id)

            if all([
                    # has_evidence,
                    has_severity,
                    has_vulns,
            ]):
                report_date = datetime_utils.get_as_str(
                    datetime_utils.get_now()
                )
                history = cast(
                    List[Dict[str, str]],
                    finding['historic_state']
                )
                history.append({
                    'analyst': analyst_email,
                    'date': report_date,
                    'state': 'SUBMITTED'
                })

                success = await finding_dal.update(finding_id, {
                    'historic_state': history
                })
            else:
                required_fields = {
                    # 'evidence': has_evidence,
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


async def get_drafts_by_group(
    group_name: str,
    attrs: Set[str] = None,
    include_deleted: bool = False
) -> List[Dict[str, FindingType]]:
    if attrs and 'historic_state' not in attrs:
        attrs.add('historic_state')
    findings = await finding_dal.get_findings_by_group(group_name, attrs)
    findings = finding_filters.filter_non_approved_findings(findings)
    if not include_deleted:
        findings = finding_filters.filter_non_deleted_findings(findings)

    return [
        finding_utils.format_finding(finding, attrs)
        for finding in findings
    ]


async def list_drafts(
    group_names: List[str],
    include_deleted: bool = False
) -> List[List[str]]:
    """Returns a list the list of finding ids associated with the groups"""
    attrs = {'finding_id', 'historic_state'}
    findings = await collect(
        get_drafts_by_group(
            group_name,
            attrs,
            include_deleted
        )
        for group_name in group_names
    )
    findings = [
        list(map(
            lambda finding: finding['finding_id'],
            group_findings
        ))
        for group_findings in findings
    ]

    return cast(List[List[str]], findings)
