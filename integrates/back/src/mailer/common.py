from aioextensions import (
    collect,
    in_thread,
)
from context import (
    FI_EMAIL_TEMPLATES,
    FI_MANDRILL_API_KEY,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    UnableToSendMail,
)
from custom_types import (
    MailContent as MailContentType,
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
)
from users import (
    domain as users_domain,
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


def get_content(template_name: str, context: MailContentType) -> str:
    template = TEMPLATES.get_template(f"{template_name}.html")
    return template.render(context)


async def get_recipient_first_name(email: str) -> str:
    first_name = email.split("@")[0]
    user_attr = await users_domain.get_attributes(email, ["first_name"])
    if user_attr and user_attr.get("first_name"):
        first_name = user_attr["first_name"]
    return str(first_name)


async def log(msg: str, **kwargs: Any) -> None:
    await in_thread(LOGGER_TRANSACTIONAL.info, msg, **kwargs)


async def send_mail_async(
    email_to: str,
    context: MailContentType,
    tags: List[str],
    subject: str,
    template_name: str,
) -> None:
    mandrill_client = mailchimp_transactional.Client(FI_MANDRILL_API_KEY)
    first_name = await get_recipient_first_name(email_to)
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
    except (ApiClientError, JSONDecodeError) as ex:
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


async def send_mails_async(
    email_to: List[str],
    context: MailContentType,
    tags: List[str],
    subject: str,
    template_name: str,
) -> None:
    test_group_list = FI_TEST_PROJECTS.split(",")
    await collect(
        [
            send_mail_async(email, context, tags, subject, template_name)
            for email in email_to
            if context.get("group", "").lower() not in test_group_list
        ]
    )
