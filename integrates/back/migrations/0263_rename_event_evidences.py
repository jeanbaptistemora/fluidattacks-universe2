# type: ignore

# pylint: disable=invalid-name
"""
Rename the event evidences to keep the consistence with the new ones

Execution Time:    2022-08-23 at 22:15:47 UTC
Finalization Time: 2022-08-23 at 22:18:48 UTC

Execution Time:    2022-08-24 at 14:40:21 UTC
Finalization Time: 2022-08-24 at 14:40:29 UTC
"""
from aioextensions import (
    collect,
    run,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_S3_MAIN_BUCKET,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    events as events_model,
)
from db_model.events.enums import (
    EventEvidenceId,
)
from db_model.events.types import (
    Event,
    EventEvidence,
    GroupEventsRequest,
)
from itertools import (
    chain,
)
import logging
import logging.config
from magic import (
    Magic,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
import os
from s3 import (
    operations as s3_ops,
)
from s3.resource import (
    get_s3_resource,
)
from settings import (
    LOGGING,
)
import tempfile
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def upload_file(
    bucket: str, file_object: object, file_name: str
) -> None:
    client = await get_s3_resource()
    try:
        await client.upload_fileobj(
            file_object,
            bucket,
            file_name,
        )
    except ClientError as ex:
        print(f"Error occurred uploading file: {ex}")
        raise


async def update_evidence(
    event: Event,
    evidence_id: EventEvidenceId,
    file: object,
    target_name: str,
    modified_date: str,
) -> None:
    mime = Magic(mime=True)
    mime_type = mime.from_file(target_name)
    extension = {
        "application/csv": ".csv",
        "image/gif": ".gif",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf",
        "application/zip": ".zip",
        "text/csv": ".csv",
        "text/plain": ".txt",
    }[mime_type]
    file_name = (
        f"{event.group_name}_{event.id}_evidence_"
        f"{str(evidence_id.value).lower()}{extension}"
    )
    full_name = f"{event.group_name}/{event.id}/{file_name}"
    await upload_file(FI_AWS_S3_MAIN_BUCKET, file, full_name)
    await events_model.update_evidence(
        event_id=event.id,
        group_name=event.group_name,
        evidence_info=EventEvidence(
            file_name=file_name,
            modified_date=datetime_utils.get_as_utc_iso_format(modified_date),
        ),
        evidence_id=evidence_id,
    )

    evidence_id_to_remove = None
    if evidence_id is EventEvidenceId.IMAGE_1:
        evidence_id_to_remove = EventEvidenceId.IMAGE
    elif evidence_id is EventEvidenceId.FILE_1:
        evidence_id_to_remove = EventEvidenceId.FILE

    if (
        evidence_id_to_remove
        and (
            evidence_to_remove := getattr(
                event.evidences,
                str(evidence_id_to_remove.value).lower(),
                None,
            )
        )
        and isinstance(evidence_to_remove, EventEvidence)
    ):
        full_name = (
            f"{event.group_name}/{event.id}/{evidence_to_remove.file_name}"
        )
        await s3_ops.remove_file(full_name)
        await events_model.update_evidence(
            event_id=event.id,
            group_name=event.group_name,
            evidence_info=None,
            evidence_id=evidence_id_to_remove,
        )


async def process_images(event: Event) -> None:
    update_image = True
    if "Masked" in event.evidences.image.file_name:
        return
    with tempfile.TemporaryDirectory() as temp_dir:
        os.makedirs(f"{temp_dir}/{event.group_name}/{event.id}", exist_ok=True)
        file_name = (
            f"{event.group_name}/{event.id}/"
            f"{event.evidences.image.file_name}"
        )
        target_name = f"{temp_dir}/{file_name}"
        try:
            await s3_ops.download_file(
                file_name=file_name,
                file_path=target_name,
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "404":
                try:
                    list_files = await s3_ops.list_files(file_name)
                    file_name = list_files[0]
                    await s3_ops.download_file(
                        file_name=file_name,
                        file_path=target_name,
                    )
                except (ClientError, IndexError):
                    update_image = False
                    await events_model.update_evidence(
                        event_id=event.id,
                        group_name=event.group_name,
                        evidence_info=None,
                        evidence_id=EventEvidenceId.IMAGE,
                    )
                    print("remove", file_name)

        if update_image:
            with open(target_name, mode="rb", encoding=None) as file:
                await update_evidence(
                    event=event,
                    evidence_id=EventEvidenceId.IMAGE_1,
                    file=file,
                    target_name=target_name,
                    modified_date=event.evidences.image.modified_date,
                )


async def process_event(event: Event) -> None:  # noqa: MC0001
    if event.evidences.file:
        update_file = True
        if "Masked" in event.evidences.file.file_name:
            return

        with tempfile.TemporaryDirectory() as temp_dir:
            os.makedirs(
                f"{temp_dir}/{event.group_name}/{event.id}", exist_ok=True
            )
            file_name = (
                f"{event.group_name}/{event.id}/"
                f"{event.evidences.file.file_name}"
            )

            target_name = f"{temp_dir}/{file_name}"
            try:
                await s3_ops.download_file(
                    file_name=file_name,
                    file_path=target_name,
                )
            except ClientError as exc:
                if exc.response["Error"]["Code"] == "404":
                    try:
                        list_files = await s3_ops.list_files(file_name)
                        file_name = list_files[0]
                        await s3_ops.download_file(
                            file_name=file_name,
                            file_path=target_name,
                        )
                    except (ClientError, IndexError):
                        update_file = False
                        await events_model.update_evidence(
                            event_id=event.id,
                            group_name=event.group_name,
                            evidence_info=None,
                            evidence_id=EventEvidenceId.FILE,
                        )
                        print("remove", file_name)

            if update_file:
                with open(target_name, mode="rb", encoding=None) as file:
                    await update_evidence(
                        event=event,
                        evidence_id=EventEvidenceId.FILE_1,
                        file=file,
                        target_name=target_name,
                        modified_date=event.evidences.file.modified_date,
                    )

    if event.evidences.image:
        await process_images(event)


async def get_group_events(
    loaders: Dataloaders, group_name: str
) -> tuple[Event, ...]:
    events = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    return events


async def main() -> None:  # noqa: MC0001
    loaders = get_new_context()
    all_organization_ids = {"ORG#unknown"}

    async for organization in orgs_domain.iterate_organizations():
        all_organization_ids.add(organization.id)

    all_group_names = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    orgs_domain.get_group_names(loaders, organization_id)
                    for organization_id in all_organization_ids
                ),
                workers=100,
            )
        )
    )
    all_events = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    get_group_events(loaders, group_name)
                    for group_name in all_group_names
                ),
                workers=50,
            )
        )
    )

    await collect(
        tuple(process_event(event) for event in all_events),
        workers=50,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
