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
from dataloaders import (
    Dataloaders,
    get_new_context,
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
from redis_cluster.operations import (
    redis_del_by_deps,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
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


async def _update_indicators(finding_id: str, group_name: str) -> None:
    await redis_del_by_deps(
        "upload_file", finding_id=finding_id, group_name=group_name
    )
    await update_unreliable_indicators_by_deps(
        EntityDependency.update_nickname,
        finding_ids=[finding_id],
    )


async def _process_vuln(
    *,
    source_nickname: str,
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

    format_old_nickname: str = f"{source_nickname}/"
    if vulnerability.where.startswith(format_old_nickname):
        format_new_nickname: str = f"{target_nickname}/"
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
    root_id: str,
    source_nickname: str,
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
                source_nickname=source_nickname,
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
    await _update_indicators(
        finding_id=finding_id,
        group_name=group_name,
    )


async def update_nickname(*, item: BatchProcessing) -> None:
    subject: str = item.subject
    root_id: str = item.entity
    info: dict[str, Any] = json.loads(item.additional_info)
    group_name: str = info["group_name"]
    source_nickname: str = info["source_nickname"]
    target_nickname: str = info["target_nickname"]
    loaders: Dataloaders = get_new_context()

    LOGGER.info(
        "Updating nickname in vulnerabilities in root", extra={"extra": info}
    )
    enforcer = await get_group_level_enforcer(subject, with_cache=False)
    if enforcer(
        group_name,
        "api_mutations_update_git_root_mutate",
    ):
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
                    root_id=root_id,
                    source_nickname=source_nickname,
                    target_nickname=target_nickname,
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
    LOGGER.info("Task completed successfully.")
