# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.event_comments.types import (
    EventComment,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.findings.types import (
    Finding,
)
from db_model.group_comments.types import (
    GroupComment,
)
from group_access import (
    domain as group_access_domain,
)
import logging
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
COMMENTS_AGE = 1


def days_since_comment(date: str) -> int:
    days = (
        datetime_utils.get_now()
        - datetime_utils.get_datetime_from_iso_str(date)
    ).days
    return days


def last_comments(
    comments: Tuple[Union[GroupComment, EventComment, FindingComment], ...],
) -> Tuple[Union[GroupComment, EventComment, FindingComment], ...]:
    return tuple(
        comment
        for comment in comments
        if days_since_comment(comment.creation_date) <= COMMENTS_AGE
    )


async def group_comments(
    loaders: Dataloaders, group_name: str
) -> Tuple[Union[GroupComment, EventComment, FindingComment], ...]:
    comments = await loaders.group_comments.load(group_name)
    return last_comments(comments)


async def instance_comments(
    loaders: Dataloaders, instance_id: str, instance_type: str
) -> Tuple[Union[GroupComment, EventComment, FindingComment], ...]:
    if instance_type == "event":
        return last_comments(await loaders.event_comments.load(instance_id))

    comments = (
        await loaders.finding_comments.load((CommentType.COMMENT, instance_id))
        + await loaders.finding_comments.load(
            (CommentType.CONSULT, instance_id)
        )
        + await loaders.finding_comments.load(
            (CommentType.VERIFICATION, instance_id)
        )
    )

    return last_comments(comments)


async def group_instance_comments(
    loaders: Dataloaders,
    group_instances: Tuple[Union[Event, Finding], ...],
    instance_type: str,
) -> Dict[str, Tuple[Union[GroupComment, EventComment, FindingComment], ...]]:
    comments = await collect(
        [
            instance_comments(loaders, instance.id, instance_type)
            for instance in group_instances
            if instance.id
        ]
    )

    comments_dic = dict(
        zip(
            [
                instance._asdict().get("title", instance.id)
                for instance in group_instances
            ],
            comments,
        )
    )

    return {
        instance: instance_comment
        for instance, instance_comment in comments_dic.items()
        if instance_comment
    }


async def finding_comments(
    loaders: Dataloaders, finding_id: str
) -> Tuple[Union[GroupComment, EventComment, FindingComment], ...]:
    comments = await loaders.finding_comments.load(finding_id)
    return last_comments(comments)


async def send_comment_digest() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)
    group_stakeholders_email = await collect(
        [
            group_access_domain.get_group_stakeholders_emails(
                loaders,
                group_name,
            )
            for group_name in groups_names
        ]
    )

    if FI_ENVIRONMENT == "development":
        groups_names = tuple(
            group_name
            for group_name in groups_names
            if group_name not in FI_TEST_PROJECTS.split(",")
        )

    groups_comments: Tuple[
        Tuple[Union[GroupComment, EventComment, FindingComment], ...], ...
    ] = await collect(
        [group_comments(loaders, group_name) for group_name in groups_names]
    )

    groups_events = await loaders.group_events.load_many(
        [
            GroupEventsRequest(group_name=group_name)
            for group_name in groups_names
        ]
    )

    events_comments: Tuple[
        Dict[
            str, Tuple[Union[GroupComment, EventComment, FindingComment], ...]
        ],
        ...,
    ] = await collect(
        [
            group_instance_comments(loaders, group_events, "event")
            for group_events in groups_events
        ]
    )

    groups_findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(groups_names)

    findings_comments: Tuple[
        Dict[
            str, Tuple[Union[GroupComment, EventComment, FindingComment], ...]
        ],
        ...,
    ] = await collect(
        [
            group_instance_comments(loaders, group_findings, "finding")
            for group_findings in groups_findings
        ]
    )

    email_data = dict(
        zip(
            groups_names,
            [
                {
                    "email_to": email_to,
                    "group_comments": group,
                    "event_comments": event,
                    "finding_comments": finding,
                }
                for email_to, group, event, finding in zip(
                    group_stakeholders_email,
                    groups_comments,
                    events_comments,
                    findings_comments,
                )
            ],
        )
    )
    LOGGER.info("- Email data to notify: %s", email_data)


async def main() -> None:
    await send_comment_digest()
