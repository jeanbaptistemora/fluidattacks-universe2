# type: ignore

# pylint: disable=invalid-name
"""
Rename the masked event evidences to keep the consistence with the new ones

Execution Time:    2022-08-24 at 14:53:44 UTC
Finalization Time: 2022-08-24 at 14:54:02 UTC
"""
from aioextensions import (
    collect,
    run,
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
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def update_evidence(
    event: Event,
    evidence_id: EventEvidenceId,
    evidence: EventEvidence,
) -> None:
    await events_model.update_evidence(
        event_id=event.id,
        group_name=event.group_name,
        evidence_info=EventEvidence(
            file_name=evidence.file_name,
            modified_date=evidence.modified_date,
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
        await events_model.update_evidence(
            event_id=event.id,
            group_name=event.group_name,
            evidence_info=None,
            evidence_id=evidence_id_to_remove,
        )


async def process_event(event: Event) -> None:  # noqa: MC0001
    if event.evidences.file:
        if "Masked" in event.evidences.file.file_name:
            await update_evidence(
                event=event,
                evidence_id=EventEvidenceId.FILE_1,
                evidence=event.evidences.file,
            )

    if event.evidences.image:
        if "Masked" in event.evidences.image.file_name:
            await update_evidence(
                event=event,
                evidence_id=EventEvidenceId.IMAGE_1,
                evidence=event.evidences.image,
            )


async def get_group_events(
    loaders: Dataloaders, group_name: str
) -> list[Event]:
    return await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )


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
