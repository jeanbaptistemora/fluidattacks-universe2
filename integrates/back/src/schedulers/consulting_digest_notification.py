from aioextensions import (
    collect,
)
from collections.abc import (
    Iterable,
)
from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
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
    FindingCommentsRequest,
)
from db_model.findings.types import (
    Finding,
)
from db_model.group_comments.types import (
    GroupComment,
)
from decorators import (
    retry_on_exceptions,
)
import logging
import logging.config
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer.groups import (
    send_mail_consulting_digest,
)
from mailer.utils import (
    get_group_emails_by_notification,
    get_organization_name,
)
from newutils import (
    datetime as datetime_utils,
    validations as validations_utils,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    TypedDict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
MAX_COMMENT_LENGTH = 500


mail_consulting_digest = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=3,
    sleep_seconds=2,
)(send_mail_consulting_digest)


class CommentsDataType(TypedDict):
    org_name: str
    email_to: tuple[str, ...]
    group_comments: tuple[GroupComment | EventComment | FindingComment, ...]
    event_comments: dict[
        str, tuple[GroupComment | EventComment | FindingComment, ...]
    ]
    finding_comments: dict[
        str, tuple[GroupComment | EventComment | FindingComment, ...]
    ]


def get_days_since_comment(date: datetime) -> int:
    return (datetime_utils.get_utc_now() - date).days


def is_last_day_comment(creation_date: datetime) -> bool:
    comments_age = 3 if datetime_utils.get_now().weekday() == 0 else 1

    return get_days_since_comment(creation_date) < comments_age


def filter_last_event_comments(
    comments: Iterable[EventComment],
) -> list[EventComment]:
    return [
        comment
        for comment in comments
        if is_last_day_comment(comment.creation_date)
    ]


def filter_last_finding_comments(
    comments: Iterable[FindingComment],
) -> list[FindingComment]:
    return [
        comment
        for comment in comments
        if is_last_day_comment(comment.creation_date)
    ]


def filter_last_group_comments(
    comments: Iterable[GroupComment],
) -> list[GroupComment]:
    return [
        comment
        for comment in comments
        if is_last_day_comment(comment.creation_date)
    ]


async def group_comments(
    loaders: Dataloaders, group_name: str
) -> tuple[GroupComment, ...]:
    comments = await loaders.group_comments.load(group_name)

    return tuple(filter_last_group_comments(comments))


async def instance_comments(
    loaders: Dataloaders, instance_id: str, instance_type: str
) -> tuple[GroupComment | EventComment | FindingComment, ...]:
    if instance_type == "event":
        return tuple(
            filter_last_event_comments(
                await loaders.event_comments.load(instance_id)
            )
        )

    comments = await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.COMMENT, finding_id=instance_id
        )
    ) + await loaders.finding_comments.load(
        FindingCommentsRequest(
            comment_type=CommentType.CONSULT, finding_id=instance_id
        )
    )

    return tuple(filter_last_finding_comments(comments))


async def group_instance_comments(
    loaders: Dataloaders,
    group_instances: Iterable[Event | Finding],
    instance_type: str,
) -> dict[str, tuple[GroupComment | EventComment | FindingComment, ...]]:
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


def unique_emails(
    comment_data: dict[str, CommentsDataType],
    email_list: tuple[str, ...],
) -> tuple[str, ...]:
    if comment_data:
        email_list += comment_data.popitem()[1]["email_to"]
        return unique_emails(comment_data, email_list)

    return tuple(set(email_list))


def format_comment(comment: str) -> str:
    if len(comment) > MAX_COMMENT_LENGTH:
        comment = f"{comment[:MAX_COMMENT_LENGTH]}..."

    return comment


def digest_comments(
    items: tuple[GroupComment | EventComment | FindingComment, ...]
) -> list[dict[str, str | None]]:
    return [
        {
            "date": datetime_utils.get_as_str(
                comment.creation_date, "%Y-%m-%d %H:%M"
            ),
            "name": "Fluid Attacks"
            if validations_utils.is_fluid_staff(comment.email)
            else comment.full_name.rstrip()
            if comment.full_name
            else comment.email.split("@")[0],
            "comment": format_comment(comment.content),
            "instance_id": comment._asdict().get("finding_id"),
        }
        for comment in items
    ]


async def send_comment_digest() -> None:
    loaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)

    if FI_ENVIRONMENT == "production":
        groups = tuple(
            group
            for group in groups
            if group.name not in FI_TEST_PROJECTS.split(",")
            and group.state.has_squad
        )

    groups_names = tuple(group.name for group in groups)
    groups_org_names = await collect(
        [
            get_organization_name(loaders, group_name)
            for group_name in groups_names
        ]
    )
    groups_stakeholders_email: tuple[list[str], ...] = await collect(
        [
            get_group_emails_by_notification(
                loaders=loaders,
                group_name=group_name,
                notification="consulting_digest",
            )
            for group_name in groups_names
        ]
    )
    groups_comments = await collect(
        [group_comments(loaders, group_name) for group_name in groups_names]
    )
    groups_events = await loaders.group_events.load_many(
        [
            GroupEventsRequest(group_name=group_name)
            for group_name in groups_names
        ]
    )
    events_comments = await collect(
        [
            group_instance_comments(loaders, group_events, "event")
            for group_events in groups_events
        ]
    )
    groups_findings = await loaders.group_findings.load_many(groups_names)
    findings_comments = await collect(
        [
            group_instance_comments(loaders, group_findings, "finding")
            for group_findings in groups_findings
        ]
    )

    groups_data: dict[str, CommentsDataType] = dict(
        zip(
            groups_names,
            [
                {
                    "org_name": org_name,
                    "email_to": tuple(email_to),
                    "group_comments": group,
                    "event_comments": event,
                    "finding_comments": finding,
                }
                for org_name, email_to, group, event, finding in zip(
                    groups_org_names,
                    groups_stakeholders_email,
                    groups_comments,
                    events_comments,
                    findings_comments,
                )
            ],
        )
    )

    groups_data = {
        group_name: data
        for (group_name, data) in groups_data.items()
        if (
            data["email_to"]
            and (
                data["group_comments"]
                or data["event_comments"]
                or data["finding_comments"]
            )
        )
    }

    for email in unique_emails(dict(groups_data), ()):
        user_content: dict[str, Any] = {
            "groups_data": {
                group_name: {
                    "org_name": data["org_name"],
                    "group_comments": digest_comments(data["group_comments"]),
                    "event_comments": {
                        event_id: digest_comments(comments)
                        for event_id, comments in data[
                            "event_comments"
                        ].items()
                    },
                    "finding_comments": {
                        finding_id: digest_comments(comments)
                        for finding_id, comments in data[
                            "finding_comments"
                        ].items()
                    },
                }
                for group_name, data in groups_data.items()
                if email in data["email_to"]
            },
            "date": datetime_utils.get_as_str(
                datetime_utils.get_now_minus_delta(), "%Y-%m-%d"
            ),
        }

        try:
            await mail_consulting_digest(
                loaders=loaders,
                context=user_content,
                email_to=email,
                email_cc=[],
            )
            LOGGER.info(
                "Consulting email sent",
                extra={"extra": {"email": email}},
            )
        except KeyError:
            LOGGER.info(
                "Key error, email not sent",
                extra={"extra": {"email": email}},
            )
            continue
    LOGGER.info("Consulting report execution finished.")


async def main() -> None:
    await send_comment_digest()
