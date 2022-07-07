from aioextensions import (
    collect,
    in_thread,
)
from context import (
    FI_EMAIL_TEMPLATES,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_CUSTOMER_SUCCESS,
    FI_MAIL_PROJECTS,
    FI_MAIL_REVIEWERS,
    FI_MANDRILL_API_KEY,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    StakeholderNotFound,
    UnableToSendMail,
)
from db_model.stakeholders.types import (
    Stakeholder,
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
from simplejson.errors import (  # type: ignore
    JSONDecodeError,
)
from typing import (
    Any,
    List,
    Optional,
)

logging.config.dictConfig(LOGGING)


# Constants
COMMENTS_TAG: List[str] = ["comments"]
DIGEST_TAG = ["digest"]
GENERAL_TAG: List[str] = ["general"]
LOGGER_ERRORS = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger("transactional")
TEMPLATES = Environment(
    loader=FileSystemLoader(FI_EMAIL_TEMPLATES), autoescape=True
)
VERIFY_TAG: List[str] = ["verify"]


def get_content(template_name: str, context: dict[str, Any]) -> str:
    template = TEMPLATES.get_template(f"{template_name}.html")
    return template.render(context)


async def get_recipient_first_name(
    loaders: Any,
    email: str,
    is_access_granted: bool = False,
) -> Optional[str]:
    first_name = email.split("@")[0]
    try:
        stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    except StakeholderNotFound:
        stakeholder = Stakeholder(
            email=email, first_name="", last_name="", is_registered=False
        )
    is_constant: bool = email.lower() in {
        *[fi_email.lower() for fi_email in FI_MAIL_CONTINUOUS.split(",")],
        *[
            fi_email.lower()
            for fi_email in FI_MAIL_CUSTOMER_SUCCESS.split(",")
        ],
        FI_MAIL_PROJECTS.lower(),
        *[fi_email.lower() for fi_email in FI_MAIL_REVIEWERS.split(",")],
    }
    is_registered = bool(stakeholder.is_registered) if stakeholder else False
    if is_constant or is_registered or is_access_granted:
        if stakeholder and stakeholder.first_name:
            return str(stakeholder.first_name)
        return str(first_name)
    return None


async def log(msg: str, **kwargs: Any) -> None:
    await in_thread(LOGGER_TRANSACTIONAL.info, msg, **kwargs)


async def send_mail_async(
    *,
    loaders: Any,
    email_to: str,
    context: dict[str, Any],
    tags: List[str],
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
    content = get_content(template_name, context)
    message = {
        "from_email": "noreply@fluidattacks.com",
        "from_name": "Fluid Attacks",
        "html": content,
        "subject": subject,
        "tags": tags,
        "to": [{"email": email_to, "name": first_name, "type": "to"}],
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
    loaders: Any,
    email_to: List[str],
    context: dict[str, Any],
    tags: List[str],
    subject: str,
    template_name: str,
    is_access_granted: bool = False,
) -> None:
    test_group_list = FI_TEST_PROJECTS.split(",")
    await collect(
        tuple(
            send_mail_async(
                loaders=loaders,
                email_to=email,
                context=context,
                tags=tags,
                subject=subject,
                template_name=template_name,
                is_access_granted=is_access_granted,
            )
            for email in email_to
            if str(context.get("group", "")).lower() not in test_group_list
        )
    )


async def send_mail_confirm_deletion(
    loaders: Any, email_to: List[str], context: dict[str, Any]
) -> None:
    await send_mails_async(
        loaders=loaders,
        email_to=email_to,
        context=context,
        tags=[],
        subject="Confirm account deletion",
        template_name="confirm_deletion",
    )
