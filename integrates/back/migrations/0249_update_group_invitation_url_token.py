# type: ignore

# pylint: disable=invalid-name
"""
Update url_token at group invitation by encoding relevant info and not
just a random string.

Also resend invitation emails.

Execution Time:    2022-07-29 at 20:42:14 UTC
Finalization Time: 2022-07-29 at 20:50:47 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from context import (
    BASE_URL,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.group_access.types import (
    GroupAccessMetadataToUpdate,
)
from db_model.groups.types import (
    Group,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from dynamodb.types import (
    Item,
)
from group_access import (
    dal as group_access_dal,
)
import logging
import logging.config
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
    group_access as group_access_utils,
    token as token_utils,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
TABLE_NAME = "FI_project_access"


async def get_access_items() -> list[Item]:
    now_epoch = datetime_utils.get_as_epoch(datetime_utils.get_now())
    filter_exp = (
        Attr("invitation").exists()
        & Attr("invitation.is_used").eq(False)
        & Attr("expiration_time").gt(now_epoch)
    )
    scan_attrs = {"FilterExpression": filter_exp}
    return await dynamodb_ops.scan(TABLE_NAME, scan_attrs)


async def process_invitation(loaders: Dataloaders, item: Item) -> None:
    group_access = group_access_utils.format_group_access(item)
    email = group_access.email
    group_name = group_access.group_name
    new_url_token = token_utils.new_encoded_jwt(
        {
            "group_name": group_name,
            "user_email": email,
        },
    )
    updated_invitation = group_access.invitation._replace(
        url_token=new_url_token
    )
    await group_access_dal.update_metadata(
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(invitation=updated_invitation),
    )

    # Resend invitation
    group: Group = await loaders.group.load(group_name)
    responsible = "integrates@fluidattacks.com"
    confirm_access_url = f"{BASE_URL}/confirm_access/{new_url_token}"
    reject_access_url = f"{BASE_URL}/reject_access/{new_url_token}"
    mail_to = [email]
    email_context: dict[str, Any] = {
        "admin": email,
        "group": group_name,
        "responsible": responsible,
        "group_description": group.description,
        "confirm_access_url": confirm_access_url,
        "reject_access_url": reject_access_url,
        "user_role": updated_invitation.role.replace("_", " "),
    }
    await groups_mail.send_mail_access_granted(loaders, mail_to, email_context)

    LOGGER_CONSOLE.info(
        "Processed",
        extra={
            "extra": {
                "email": group_access.email,
                "group_name": group_access.group_name,
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    items = await get_access_items()
    LOGGER_CONSOLE.info(
        "Invitations still pending",
        extra={"extra": {"scanned": len(items)}},
    )

    await collect(
        (process_invitation(loaders, item) for item in items),
        workers=8,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
