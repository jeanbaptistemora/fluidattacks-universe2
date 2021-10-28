import authz
from batch.dal import (
    delete_action,
    is_action_by_key,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
)
import logging
import logging.config
from newutils.passphrase import (
    get_passphrase,
)
from newutils.reports import (
    sign_url,
    upload_report,
)
from notifications import (
    domain as notifications_domain,
)
import os
from reports import (
    domain as reports_domain,
)
from settings import (
    LOGGING,
    NOEXTRA,
)
from typing import (
    Dict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger("transactional")


async def get_report(*, item: BatchProcessing, passphrase: str) -> str:
    report_file_name: str = ""
    try:
        report_file_name = await reports_domain.get_group_report_url(
            report_type=item.additional_info,
            group_name=item.entity,
            passphrase=passphrase,
            user_email=item.subject,
        )
        uploaded_file_name = await upload_report(report_file_name)
    except ErrorUploadingFileS3 as exc:
        LOGGER.exception(
            exc,
            extra=dict(
                extra=dict(
                    group_name=item.entity,
                    user_email=item.subject,
                )
            ),
        )
        return ""
    else:
        return uploaded_file_name
    finally:
        if os.path.exists(report_file_name):
            os.unlink(report_file_name)


async def send_report(
    *,
    item: BatchProcessing,
    passphrase: str,
    report_type: str,
    report_url: str,
) -> None:
    translations: Dict[str, str] = {
        "DATA": "Group Data",
        "PDF": "Executive",
        "XLS": "Technical",
    }
    is_in_db = await is_action_by_key(key=item.key)
    enforcer = await authz.get_group_level_enforcer(item.subject)
    if is_in_db and enforcer(
        item.entity, "api_resolvers_query_report__get_url_group_report"
    ):
        message = (
            f"Send {item.additional_info} report requested by "
            f"{item.subject} for group {item.entity}"
        )
        LOGGER_TRANSACTIONAL.info(":".join([item.subject, message]), **NOEXTRA)
        await notifications_domain.new_password_protected_report(
            item.subject,
            item.entity,
            passphrase,
            translations[report_type.upper()],
            await sign_url(report_url),
        )
        await delete_action(
            action_name=item.action_name,
            additional_info=item.additional_info,
            entity=item.entity,
            subject=item.subject,
            time=item.time,
        )


async def generate_report(*, item: BatchProcessing) -> None:
    message = (
        f"Processing {item.additional_info} report requested by "
        f"{item.subject} for group {item.entity}"
    )
    LOGGER_TRANSACTIONAL.info(":".join([item.subject, message]), **NOEXTRA)
    enforcer = await authz.get_group_level_enforcer(item.subject)
    if enforcer(
        item.entity, "api_resolvers_query_report__get_url_group_report"
    ):
        passphrase = get_passphrase(4)
        report_url = await get_report(item=item, passphrase=passphrase)
        if report_url:
            await send_report(
                item=item,
                passphrase=passphrase,
                report_type=item.additional_info,
                report_url=report_url,
            )
    else:
        LOGGER.error(
            "Access denied",
            extra=dict(
                extra=dict(
                    action=item.action_name,
                    group_name=item.entity,
                    user_email=item.subject,
                )
            ),
        )
        await delete_action(
            action_name=item.action_name,
            additional_info=item.additional_info,
            entity=item.entity,
            subject=item.subject,
            time=item.time,
        )
