# pylint: disable=invalid-name
"""
Take findings latests states to the metadata item

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.findings.types import (
    Finding,
)
from db_model.findings.utils import (
    format_state_item,
    format_unreliable_indicators_item,
    format_verification_item,
)
from db_model.groups.types import (
    Group,
)
from dynamodb import (
    keys,
    operations,
)
import logging
import logging.config
from organizations.domain import (
    get_all_active_groups,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_finding(finding: Finding) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": finding.group_name, "id": finding.id},
    )
    metadata_item = {
        "state": format_state_item(finding.state),
        "creation": format_state_item(finding.creation),
        "unreliable_indicators": format_unreliable_indicators_item(
            finding.unreliable_indicators
        ),
    }
    if finding.approval:
        metadata_item["approval"] = format_state_item(finding.approval)
    if finding.submission:
        metadata_item["submission"] = format_state_item(finding.submission)
    if finding.verification:
        metadata_item["verification"] = format_verification_item(
            finding.verification
        )
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=metadata_item,
        key=metadata_key,
        table=TABLE,
    )


async def process_group(
    *,
    group: Group,
    loaders: Dataloaders,
    progress: float,
) -> None:
    group_findings: tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group.name)
    await collect(
        tuple(process_finding(finding=finding) for finding in group_findings),
        workers=16,
    )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group.name,
                "drafts_and_findings": len(group_findings),
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    active_groups = await get_all_active_groups(loaders)
    LOGGER_CONSOLE.info(
        "Active groups",
        extra={"extra": {"groups_len": len(active_groups)}},
    )

    await collect(
        tuple(
            process_group(
                group=group,
                loaders=loaders,
                progress=count / len(active_groups),
            )
            for count, group in enumerate(active_groups)
        ),
        workers=4,
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
