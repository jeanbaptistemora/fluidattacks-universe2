""" Asynchronous task execution scheduler for FLUIDIntegrates """
# pylint: disable=too-many-lines

# Standard libraries
import logging
import logging.config
from collections import (
    defaultdict,
)
from decimal import Decimal
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    List,
    Union,
    Tuple,
)

# Third party libraries
import bugsnag
from aioextensions import (
    collect,
    schedule,
)

# Local libraries
from back.settings import LOGGING
from backend import mailer
from backend.api import get_new_context
from backend.typing import (
    Event as EventType,
    Historic as HistoricType,
    MailContent as MailContentType,
    Project as ProjectType,
)
from events import domain as events_domain
from findings import domain as findings_domain
from groups import domain as groups_domain
from group_access import domain as group_access_domain
from newutils import (
    findings as findings_utils,
)
from organizations import domain as orgs_domain
from tags import domain as tags_domain
from __init__ import (
    BASE_URL,
    FI_TEST_PROJECTS,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS,
    FI_ENVIRONMENT,
    FI_BUGSNAG_API_KEY_SCHEDULER
)

logging.config.dictConfig(LOGGING)

bugsnag.configure(
    api_key=FI_BUGSNAG_API_KEY_SCHEDULER,
    project_root=BASE_URL,
    release_stage=FI_ENVIRONMENT,
)
bugsnag.start_session()

LOGGER = logging.getLogger(__name__)


def is_not_a_fluidattacks_email(email: str) -> bool:
    return 'fluidattacks.com' not in email


def remove_fluid_from_recipients(emails: List[str]) -> List[str]:
    new_email_list = list(filter(is_not_a_fluidattacks_email, emails))
    return new_email_list


def is_a_unsolved_event(event: EventType) -> bool:
    return cast(
        List[Dict[str, str]],
        event.get('historic_state', [{}])
    )[-1].get('state', '') == 'CREATED'


async def get_unsolved_events(project: str) -> List[EventType]:
    events = await events_domain.list_group_events(project)
    event_list = await collect(
        events_domain.get_event(event)
        for event in events
    )
    unsolved_events = list(filter(is_a_unsolved_event, event_list))
    return unsolved_events


def extract_info_from_event_dict(event_dict: EventType) -> EventType:
    event_dict = {
        'type': event_dict.get('event_type', ''),
        'details': event_dict.get('detail', '')
    }
    return event_dict


async def send_unsolved_events_email(context: Any, group_name: str) -> None:
    group_loader = context.group_all
    organization_loader = context.organization
    mail_to = []
    events_info_for_email = []
    project_info = await groups_domain.get_attributes(
        group_name, ['historic_configuration']
    )
    historic_configuration = cast(
        HistoricType,
        project_info.get('historic_configuration', [{}])
    )
    if (project_info and
            historic_configuration[-1].get('type', '') == 'continuous'):
        mail_to = await get_external_recipients(group_name)
        mail_to.append(FI_MAIL_PROJECTS)
        unsolved_events = await get_unsolved_events(group_name)
        events_info_for_email = [
            extract_info_from_event_dict(x)
            for x in unsolved_events
        ]
    group = await group_loader.load(group_name)
    org_id = group['organization']
    organization = await organization_loader.load(org_id)
    org_name = organization['name']
    context_event: MailContentType = {
        'project': group_name.capitalize(),
        'organization': org_name,
        'events_len': int(len(events_info_for_email)),
        'event_url': f'{BASE_URL}/orgs/{org_name}/groups/{group_name}/events'
    }
    if context_event['events_len'] and mail_to:
        scheduler_send_mail(
            mailer.send_mail_unsolved_events,
            mail_to,
            context_event
        )


async def get_external_recipients(project: str) -> List[str]:
    recipients = await group_access_domain.get_managers(project)
    return remove_fluid_from_recipients(recipients)


def calculate_tag_indicators(
        tag: str,
        tags_dict: Dict[str, List[ProjectType]],
        indicator_list: List[str]) -> Dict[str, Union[Decimal, List[str]]]:
    tag_info: Dict[str, Union[Decimal, List[str]]] = {}
    for indicator in indicator_list:
        if 'max' in indicator:
            tag_info[indicator] = Decimal(
                max([
                    cast(Decimal, group.get(indicator, Decimal('0.0')))
                    for group in tags_dict[tag]
                ])
            ).quantize(Decimal('0.1'))
        elif 'mean' in indicator:
            tag_info[indicator] = Decimal(
                sum([
                    cast(Decimal, group.get(indicator, Decimal('0.0')))
                    for group in tags_dict[tag]
                ]) / Decimal(len(tags_dict[tag]))
            ).quantize(Decimal('0.1'))
        else:
            tag_info[indicator] = Decimal(
                min([
                    cast(Decimal, group.get(indicator, Decimal('inf')))
                    for group in tags_dict[tag]
                ])
            ).quantize(Decimal('0.1'))
        tag_info['projects'] = [
            str(group['name']) for group in tags_dict[tag]
        ]
    return tag_info


async def get_remediated_findings() -> None:
    """Summary mail send with findings that have not been verified yet."""
    active_projects = await groups_domain.get_active_groups()
    findings = []
    pending_verification_findings = await collect(
        findings_domain.get_pending_verification_findings(
            get_new_context(),
            project
        )
        for project in active_projects
    )
    for project_findings in pending_verification_findings:
        findings += project_findings

    if findings:
        try:
            mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
            context: MailContentType = {'findings': list(), 'total': 0}
            for finding in findings:
                cast(
                    List[Dict[str, str]],
                    context['findings']
                ).append({
                    'finding_name': finding['finding'],
                    'finding_url': (
                        f'{BASE_URL}/groups/'
                        f'{str.lower(str(finding["project_name"]))}/'
                        f'{finding["finding_id"]}/description'
                    ),
                    'project': str.upper(str(finding['project_name']))
                })
            context['total'] = len(findings)
            scheduler_send_mail(
                mailer.send_mail_new_remediated,
                mail_to,
                context
            )
        except (TypeError, KeyError) as ex:
            LOGGER.exception(ex, extra={'extra': locals()})


async def get_new_releases() -> None:  # pylint: disable=too-many-locals
    """Summary mail send with findings that have not been released yet."""
    context = get_new_context()
    group_loader = context.group_all
    organization_loader = context.organization
    test_groups = FI_TEST_PROJECTS.split(',')
    groups = await groups_domain.get_active_groups()
    email_context: MailContentType = (
        defaultdict(list)
    )
    cont = 0
    groups = [
        group
        for group in groups
        if group not in test_groups
    ]
    list_drafts = await findings_domain.list_drafts(groups)
    group_drafts = await collect(
        findings_domain.get_findings_async(drafts)
        for drafts in list_drafts
    )
    for group_name, finding_requests in zip(groups, group_drafts):
        if group_name not in test_groups:
            try:
                for finding in finding_requests:
                    is_finding_released = findings_utils.is_released(finding)
                    if not is_finding_released:
                        group = await group_loader.load(group_name)
                        org_id = group['organization']
                        organization = await organization_loader.load(org_id)
                        org_name = organization['name']
                        submission = finding.get('historicState')
                        status = submission[-1].get('state')
                        category = (
                            'unsubmitted'
                            if status in ('CREATED', 'REJECTED')
                            else 'unreleased'
                        )
                        cast(
                            List[Dict[str, str]],
                            email_context[category]
                        ).append({
                            'finding_name': finding.get('finding'),
                            'finding_url': (
                                f'{BASE_URL}/orgs/{org_name}/groups/'
                                f'{group_name}/drafts/'
                                f'{finding.get("findingId")}/description'
                            ),
                            'project': group_name.upper(),
                            'organization': org_name
                        })
                        cont += 1
            except (TypeError, KeyError) as ex:
                LOGGER.exception(ex, extra={'extra': locals()})
        else:
            # ignore test projects
            pass
    if cont > 0:
        email_context['total_unreleased'] = len(
            cast(List[Dict[str, str]], email_context['unreleased'])
        )
        email_context['total_unsubmitted'] = len(
            cast(List[Dict[str, str]], email_context['unsubmitted'])
        )
        approvers = FI_MAIL_REVIEWERS.split(',')
        mail_to = [FI_MAIL_PROJECTS]
        mail_to.extend(approvers)
        scheduler_send_mail(
            mailer.send_mail_new_releases,
            mail_to,
            email_context
        )


async def send_unsolved_to_all() -> None:
    """Send email with unsolved events to all projects """
    context = get_new_context()
    projects = await groups_domain.get_active_groups()
    await collect(
        send_unsolved_events_email(context, project)
        for project in projects
    )


async def update_organization_indicators(
    context: Any,
    organization_name: str,
    groups: List[str]
) -> Tuple[bool, List[str]]:
    group_findings_loader = context.group_findings

    success: List[bool] = []
    updated_tags: List[str] = []
    indicator_list: List[str] = [
        'max_open_severity',
        'mean_remediate',
        'mean_remediate_critical_severity',
        'mean_remediate_high_severity',
        'mean_remediate_low_severity',
        'mean_remediate_medium_severity',
        'last_closing_date'
    ]
    tags_dict: Dict[str, List[ProjectType]] = defaultdict(list)
    groups_attrs = await collect(
        groups_domain.get_attributes(
            group,
            indicator_list + ['tag']
        )
        for group in groups
    )
    group_findings = await group_findings_loader.load_many(groups)
    for index, group in enumerate(groups):
        groups_attrs[index]['max_severity'] = Decimal(max(
            [
                float(finding.get('cvss_temporal', 0.0))
                for finding in group_findings[index]
            ]
            if group_findings[index]
            else [0.0]
        )).quantize(Decimal('0.1'))
        groups_attrs[index]['name'] = group
        for tag in groups_attrs[index]['tag']:
            tags_dict[tag].append(groups_attrs[index])
    for tag in tags_dict:
        updated_tags.append(tag)
        tag_info = calculate_tag_indicators(
            tag, tags_dict, indicator_list + ['max_severity']
        )
        success.append(
            await tags_domain.update(organization_name, tag, tag_info)
        )
    return all(success), updated_tags


async def update_portfolios() -> None:
    """
    Update portfolios metrics
    """
    context = get_new_context()
    group_loader = context.group_all
    async for _, org_name, org_groups in \
            orgs_domain.iterate_organizations_and_groups():
        org_tags = await context.organization_tags.load(org_name)
        org_groups_attrs = await group_loader.load_many(
            list(org_groups)
        )
        tag_groups: List[str] = [
            str(group['name'])
            for group in org_groups_attrs
            if group['project_status'] == 'ACTIVE' and group['tags']
        ]
        success, updated_tags = await update_organization_indicators(
            context,
            org_name,
            tag_groups
        )
        if success:
            deleted_tags = [
                tag['tag']
                for tag in org_tags
                if tag['tag'] not in updated_tags
            ]
            await collect(
                tags_domain.delete(org_name, str(tag)) for tag in deleted_tags
            )
        else:
            LOGGER.error(
                '[scheduler]: error updating portfolio indicators',
                extra={'extra': {'organization': org_name}}
            )


def scheduler_send_mail(
    send_mail_function: Callable,
    mail_to: List[str],
    mail_context: MailContentType
) -> None:
    schedule(
        send_mail_function(mail_to, mail_context)
    )
