from aioextensions import (
    collect,
    in_thread,
)
from context import (
    FI_EMAIL_TEMPLATES,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_COS,
    FI_MAIL_CTO,
    FI_MAIL_CUSTOMER_EXPERIENCE,
    FI_MAIL_CUSTOMER_SUCCESS,
    FI_MAIL_PRODUCTION,
    FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS,
    FI_MAIL_TELEMARKETING,
    FI_MANDRILL_API_KEY,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
)
from http.client import (
    RemoteDisconnected,
)
from jinja2 import (
    Environment,
    FileSystemLoader,
)
import json
import logging
import logging.config
import mailchimp_transactional
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from newutils import (
    datetime as datetime_utils,
)
from settings import (
    LOGGING,
)
from simplejson.errors import (
    JSONDecodeError,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)


# Constants
COMMENTS_TAG: list[str] = ["comments"]
GENERAL_TAG: list[str] = ["general"]
LOGGER_ERRORS = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger("transactional")
TEMPLATES = Environment(
    autoescape=True,
    loader=FileSystemLoader(FI_EMAIL_TEMPLATES),
    lstrip_blocks=True,
    trim_blocks=True,
)
VERIFY_TAG: list[str] = ["verify"]


def get_content(template_name: str, context: dict[str, Any]) -> str:
    template = TEMPLATES.get_template(f"{template_name}.html")
    return template.render(context)


async def get_recipient_first_name(
    loaders: Dataloaders,
    email: str,
    is_access_granted: bool = False,
) -> str | None:
    first_name = email.split("@")[0]
    stakeholder = await loaders.stakeholder.load(email)
    is_constant: bool = email.lower() in {
        *[fi_email.lower() for fi_email in FI_MAIL_CONTINUOUS.split(",")],
        *[fi_email.lower() for fi_email in FI_MAIL_COS.split(",")],
        *[fi_email.lower() for fi_email in FI_MAIL_CTO.split(",")],
        *[
            fi_email.lower()
            for fi_email in FI_MAIL_CUSTOMER_EXPERIENCE.split(",")
        ],
        *[
            fi_email.lower()
            for fi_email in FI_MAIL_CUSTOMER_SUCCESS.split(",")
        ],
        *[fi_email.lower() for fi_email in FI_MAIL_PRODUCTION.split(",")],
        FI_MAIL_PROJECTS.lower(),
        *[fi_email.lower() for fi_email in FI_MAIL_REVIEWERS.split(",")],
        FI_MAIL_TELEMARKETING.lower(),
    }
    is_registered = bool(stakeholder.is_registered) if stakeholder else False
    if is_constant or is_registered or is_access_granted:
        if stakeholder and stakeholder.first_name:
            return str(stakeholder.first_name)
        return str(first_name)
    return None


async def get_recipients(
    *,
    loaders: Dataloaders,
    email_to: str,
    email_cc: list[str] | None,
    first_name: str,
    is_access_granted: bool,
) -> list[dict[str, Any]]:
    email_list = [{"email": email_to, "name": first_name, "type": "to"}]
    if email_cc:
        for email in email_cc:
            if name := await get_recipient_first_name(
                loaders, email, is_access_granted
            ):
                email_list.append({"email": email, "name": name, "type": "cc"})
    return email_list


async def log(msg: str, **kwargs: Any) -> None:
    await in_thread(LOGGER_TRANSACTIONAL.info, msg, **kwargs)


async def send_mail_async(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    email_to: str,
    email_cc: list[str] | None = None,
    context: dict[str, Any],
    tags: list[str],
    subject: str,
    template_name: str,
    is_access_granted: bool = False,
) -> None:
    mandrill_client = mailchimp_transactional.Client(FI_MANDRILL_API_KEY)
    first_name = await get_recipient_first_name(
        loaders, email_to, is_access_granted=is_access_granted
    )
    if not first_name:
        return
    year = datetime_utils.get_as_str(datetime_utils.get_now(), "%Y")
    context["name"] = first_name
    context["year"] = year
    context["mailto"] = email_to
    content = get_content(template_name, context)
    to_list: list[dict[str, Any]] = await get_recipients(
        loaders=loaders,
        email_to=email_to,
        first_name=first_name,
        email_cc=email_cc,
        is_access_granted=is_access_granted,
    )
    message = {
        "from_email": "noreply@fluidattacks.com",
        "from_name": "Fluid Attacks",
        "html": content,
        "subject": subject,
        "tags": tags,
        "to": to_list,
        "preserve_recipients": True,
    }
    try:
        response = mandrill_client.messages.send({"message": message})
        await log(
            "[mailer]: mail sent",
            extra={
                "extra": {
                    "email_to": email_to,
                    "template": template_name,
                    "subject": subject,
                    "tags": json.dumps(tags),
                    "response": response,
                }
            },
        )
    except (ApiClientError, JSONDecodeError, RemoteDisconnected) as ex:
        LOGGER_ERRORS.exception(
            ex,
            extra={
                "extra": {
                    "email_to": email_to,
                    "template": template_name,
                    "subject": subject,
                    "context": context,
                }
            },
        )
        raise UnableToSendMail() from ex


async def send_mails_async(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    email_to: list[str],
    subject: str,
    template_name: str,
    context: dict[str, Any] | None = None,
    email_cc: list[str] | None = None,
    is_access_granted: bool = False,
    tags: list[str] | None = None,
) -> None:
    test_group_list = FI_TEST_PROJECTS.split(",") if FI_TEST_PROJECTS else []
    context = context if context else {}
    await collect(
        tuple(
            send_mail_async(
                loaders=loaders,
                email_to=email,
                email_cc=email_cc,
                context=context,
                tags=tags if tags else [],
                subject=subject,
                template_name=template_name,
                is_access_granted=is_access_granted,
            )
            for email in email_to
            if str(context.get("group", context.get("group_name", ""))).lower()
            not in test_group_list
        )
    )


async def send_mail_confirm_deletion(
    loaders: Dataloaders, email_to: list[str], context: dict[str, Any]
) -> None:
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context=context,
        subject="Confirm account deletion",
        template_name="confirm_deletion",
    )
