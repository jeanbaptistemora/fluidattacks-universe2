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
from db_model import (
    findings as findings_model,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingState,
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
from newutils import (
    datetime as datetime_utils,
)
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
import uuid

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
    target_group_name: str,
    finding_vulns: Tuple[str, Iterator[Dict[str, Any]]],
) -> None:
    source_finding_id, vulns = finding_vulns
    source_finding: Finding = await loaders.finding_new.load(source_finding_id)
    target_group_findings: Tuple[
        Finding, ...
    ] = await loaders.group_findings_new.load(target_group_name)
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
    else:
        target_finding_id = str(uuid.uuid4())
        await findings_model.add(
            finding=Finding(
                affected_systems=source_finding.affected_systems,
                hacker_email=source_finding.hacker_email,
                attack_vector_description=(
                    source_finding.attack_vector_description
                ),
                description=source_finding.description,
                group_name=target_group_name,
                id=target_finding_id,
                state=FindingState(
                    modified_by=source_finding.hacker_email,
                    modified_date=datetime_utils.get_iso_date(),
                    source=source_finding.state.source,
                    status=FindingStateStatus.CREATED,
                ),
                recommendation=source_finding.recommendation,
                requirements=source_finding.requirements,
                severity=source_finding.severity,
                title=source_finding.title,
                threat=source_finding.threat,
            )
        )
        await process_vulns(tuple(vulns), target_finding_id)


async def move_root(*, item: BatchProcessing) -> None:
    target_group_name = item.entity
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
            process_finding(loaders, target_group_name, finding_vulns)
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
