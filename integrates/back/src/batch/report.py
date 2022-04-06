from batch.dal import (
    delete_action,
    is_action_by_key,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
    UnavailabilityError,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from decorators import (
    retry_on_exceptions,
)
import json
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
    Any,
    Dict,
    Set,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger("transactional")


upload_report_file = retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    max_attempts=4,
    sleep_seconds=1,
)(upload_report)


async def get_report(
    *,
    item: BatchProcessing,
    passphrase: str,
    report_type: str,
    treatments: Set[VulnerabilityTreatmentStatus],
) -> str:
    report_file_name: str = ""
    try:
        report_file_name = await reports_domain.get_group_report_url(
            report_type=report_type,
            group_name=item.entity,
            passphrase=passphrase,
            user_email=item.subject,
            treatments=treatments,
        )
        uploaded_file_name = await upload_report_file(report_file_name)
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
        "CERT": "Certificate",
        "DATA": "Group Data",
        "PDF": "Executive",
        "XLS": "Technical",
    }
    is_in_db = await is_action_by_key(key=item.key)
    if is_in_db:
        message = (
            f"Send {report_type} report requested by "
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
    additional_info: Dict[str, Any] = json.loads(item.additional_info)
    report_type: str = additional_info["report_type"]
    message = (
        f"Processing {report_type} report requested by "
        f"{item.subject} for group {item.entity}"
    )
    LOGGER_TRANSACTIONAL.info(":".join([item.subject, message]), **NOEXTRA)
    treatments = {
        VulnerabilityTreatmentStatus[treatment]
        for treatment in additional_info["treatments"]
    }
    passphrase = get_passphrase(4)
    report_url = await get_report(
        item=item,
        passphrase=passphrase,
        report_type=report_type,
        treatments=treatments,
    )
    if report_url:
        await send_report(
            item=item,
            passphrase=passphrase,
            report_type=report_type,
            report_url=report_url,
        )
