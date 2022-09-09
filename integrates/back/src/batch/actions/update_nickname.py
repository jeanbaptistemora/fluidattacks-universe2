# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from authz import (
    get_group_level_enforcer,
)
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    FindingNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.types import (
    Root,
    RootState,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
)
from db_model.vulnerabilities.update import (
    update_metadata,
)
import itertools
import json
import logging
import logging.config
from operator import (
    attrgetter,
)
from settings import (
    LOGGING,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _process_vuln(
    *,
    nicknames: set[str],
    target_nickname: str,
    vulnerability: Vulnerability,
) -> None:
    LOGGER.info(
        "Processing vulnerability",
        extra={
            "extra": {
                "vulnerability_id": vulnerability.id,
            }
        },
    )

    format_new_nickname: str = f"{target_nickname}/"
    if vulnerability.where.startswith(format_new_nickname):
        return

    slash_index = vulnerability.where.find("/")
    old_nickname = vulnerability.where[:slash_index]
    format_old_nickname = f"{old_nickname}/"
    if old_nickname in nicknames:
        await update_metadata(
            finding_id=vulnerability.finding_id,
            vulnerability_id=vulnerability.id,
            metadata=VulnerabilityMetadataToUpdate(
                where=vulnerability.where.replace(
                    format_old_nickname, format_new_nickname, 1
                )
            ),
        )


async def _process_finding(
    *,
    finding_id: str,
    group_name: str,
    nicknames: set[str],
    root_id: str,
    target_nickname: str,
    vulnerabilities: tuple[Vulnerability, ...],
) -> None:
    filter_vulnerabililities: tuple[Vulnerability, ...] = tuple(
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability.type == VulnerabilityType.LINES
    )
    if len(filter_vulnerabililities) == 0:
        return

    LOGGER.info(
        "Processing finding",
        extra={
            "extra": {
                "group_name": group_name,
                "root_id": root_id,
                "finding_id": finding_id,
                "vulnerabilities": len(filter_vulnerabililities),
            }
        },
    )

    await collect(
        tuple(
            _process_vuln(
                nicknames=nicknames,
                target_nickname=target_nickname,
                vulnerability=vulnerability,
            )
            for vulnerability in filter_vulnerabililities
            if vulnerability.state.status != VulnerabilityStateStatus.DELETED
        ),
        workers=10,
    )

    LOGGER.info(
        "Updating finding indicators",
        extra={
            "extra": {
                "group_name": group_name,
                "finding_id": finding_id,
            }
        },
    )
    try:
        await update_unreliable_indicators_by_deps(
            EntityDependency.update_nickname,
            finding_ids=[finding_id],
        )
    except FindingNotFound as ex:
        LOGGER.exception(
            ex,
            extra={
                "extra": dict(
                    finding_id=finding_id,
                    group_name=group_name,
                )
            },
        )


async def update_nickname(*, item: BatchProcessing) -> None:
    subject: str = item.subject
    root_id: str = item.entity
    group_name: str = json.loads(item.additional_info).get("group_name", "")
    loaders: Dataloaders = get_new_context()

    LOGGER.info(
        "Updating nickname in vulnerabilities in root", extra={"extra": item}
    )
    enforcer = await get_group_level_enforcer(loaders, subject)
    if enforcer(
        group_name,
        "api_mutations_update_git_root_mutate",
    ):
        root: Root = await loaders.root.load((group_name, root_id))
        historic_states: tuple[
            RootState, ...
        ] = await loaders.root_historic_states.load(root.id)
        nicknames: set[str] = set(
            state.nickname or "" for state in historic_states
        )
        root_vulnerabilities: tuple[
            Vulnerability, ...
        ] = await loaders.root_vulnerabilities.load(root_id)
        LOGGER.info(
            "Number of vulnerabilities in root",
            extra={
                "extra": {
                    "vulnerabilities": len(root_vulnerabilities),
                },
            },
        )
        vulnerabilities_by_finding = itertools.groupby(
            sorted(root_vulnerabilities, key=attrgetter("finding_id")),
            key=attrgetter("finding_id"),
        )
        await collect(
            tuple(
                _process_finding(
                    finding_id=finding_id,
                    group_name=group_name,
                    nicknames=nicknames,
                    root_id=root_id,
                    target_nickname=root.state.nickname,
                    vulnerabilities=tuple(vulnerabilities),
                )
                for finding_id, vulnerabilities in vulnerabilities_by_finding
            ),
            workers=10,
        )

    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
    LOGGER.info("Update nickname task completed successfully.")
