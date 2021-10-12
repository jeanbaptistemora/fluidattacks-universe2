from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.types import (
    RootItem,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
    Table,
)
import itertools
from operator import (
    itemgetter,
)
from roots import (
    dal as roots_dal,
)
from typing import (
    Any,
    Dict,
    Iterator,
    Tuple,
)

VULNS_TABLE = Table(
    facets={},
    indexes={},
    name="FI_vulnerabilities",
    primary_key=PrimaryKey(partition_key="finding_id", sort_key="UUID"),
)


async def process_vulns(
    vulns: Tuple[Dict[str, Any], ...],
    target_finding_id: str,
) -> None:
    await operations.batch_write_item(
        items=tuple(
            {**vuln, "finding_id": target_finding_id} for vuln in vulns
        ),
        table=VULNS_TABLE,
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(partition_key=vuln["finding_id"], sort_key=vuln["UUID"])
            for vuln in vulns
        ),
        table=VULNS_TABLE,
    )


async def process_finding(
    loaders: Any,
    target_group: str,
    finding_vulns: Tuple[str, Iterator[Dict[str, Any]]],
) -> None:
    source_finding_id, vulns = finding_vulns
    source_finding: Finding = await loaders.finding_new.load(source_finding_id)
    target_group_findings: Tuple[
        Finding, ...
    ] = await loaders.group_findings_new.load(target_group)
    target_finding = next(
        (
            finding
            for finding in target_group_findings
            if finding.title == source_finding.title
        ),
        None,
    )

    if target_finding:
        await process_vulns(tuple(vulns), target_finding.id)


async def move_root(*, item: BatchProcessing) -> None:
    target_group = item.entity
    group_name, root_id = item.additional_info.split("/")
    loaders = get_new_context()
    root: RootItem = await loaders.root.load((group_name, root_id))
    vulns = await roots_dal.get_root_vulns(
        loaders=loaders, group_name=group_name, nickname=root.state.nickname
    )
    vulns_by_finding = itertools.groupby(
        sorted(vulns, key=itemgetter("finding_id")),
        key=itemgetter("finding_id"),
    )

    await collect(
        tuple(
            process_finding(loaders, target_group, finding_vulns)
            for finding_vulns in vulns_by_finding
        )
    )
    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
