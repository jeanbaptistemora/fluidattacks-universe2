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
from mailer.common import (
    GENERAL_TAG,
    send_mails_async,
)
from newutils import (
    datetime as datetime_utils,
)
from operator import (
    itemgetter,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from roots import (
    dal as roots_dal,
)
from typing import (
    Any,
    Dict,
    Tuple,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
import uuid
from vulnerabilities import (
    domain as vulns_domain,
)

VULNS_TABLE = Table(
    facets={},
    indexes={},
    name="FI_vulnerabilities",
    primary_key=PrimaryKey(partition_key="finding_id", sort_key="UUID"),
)


async def update_indicators(finding_id: str, group_name: str) -> None:
    await redis_del_by_deps(
        "upload_file", finding_id=finding_id, group_name=group_name
    )
    await update_unreliable_indicators_by_deps(
        EntityDependency.upload_file, finding_id=finding_id
    )


async def process_vulns(
    vulns: Tuple[Dict[str, Any], ...],
    target_finding_id: str,
) -> None:
    await operations.batch_write_item(
        items=tuple(
            {
                **vuln,
                "finding_id": target_finding_id,
                "UUID": str(uuid.uuid4()),
            }
            for vuln in vulns
        ),
        table=VULNS_TABLE,
    )
    await collect(
        tuple(vulns_domain.close_by_exclusion(vuln) for vuln in vulns)
    )


async def process_finding(
    loaders: Any,
    source_group_name: str,
    target_group_name: str,
    source_finding_id: str,
    vulns: Tuple[Dict[str, Any], ...],
) -> None:
    source_finding: Finding = await loaders.finding.load(source_finding_id)
    target_group_findings: Tuple[
        Finding, ...
    ] = await loaders.group_findings.load(target_group_name)
    target_finding = next(
        (
            finding
            for finding in target_group_findings
            if finding.title == source_finding.title
        ),
        None,
    )

    if target_finding:
        target_finding_id = target_finding.id
    else:
        target_finding_id = str(uuid.uuid4())
        initial_state = FindingState(
            modified_by=source_finding.hacker_email,
            modified_date=datetime_utils.get_iso_date(),
            source=source_finding.state.source,
            status=FindingStateStatus.CREATED,
        )
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
                state=initial_state,
                recommendation=source_finding.recommendation,
                requirements=source_finding.requirements,
                severity=source_finding.severity,
                title=source_finding.title,
                threat=source_finding.threat,
            )
        )
        if source_finding.submission:
            await findings_model.update_state(
                current_value=initial_state,
                finding_id=target_finding_id,
                group_name=target_group_name,
                state=source_finding.submission,
            )
        await findings_model.update_state(
            current_value=source_finding.submission,
            finding_id=target_finding_id,
            group_name=target_group_name,
            state=source_finding.approval,
        )

    await process_vulns(vulns, target_finding_id)
    await collect(
        (
            update_indicators(source_finding_id, source_group_name),
            update_indicators(target_finding_id, target_group_name),
        )
    )


async def move_root(*, item: BatchProcessing) -> None:
    target_group_name = item.entity
    source_group_name, root_id = item.additional_info.split("/")
    loaders = get_new_context()
    root: RootItem = await loaders.root.load((source_group_name, root_id))
    root_vulns = await roots_dal.get_root_vulns(
        loaders=loaders,
        group_name=source_group_name,
        nickname=root.state.nickname,
    )
    vulns_by_finding = itertools.groupby(
        sorted(root_vulns, key=itemgetter("finding_id")),
        key=itemgetter("finding_id"),
    )

    await collect(
        tuple(
            process_finding(
                loaders,
                source_group_name,
                target_group_name,
                source_finding_id,
                tuple(vulns),
            )
            for source_finding_id, vulns in vulns_by_finding
        )
    )
    await send_mails_async(
        email_to=[item.subject],
        context={
            "group": source_group_name,
            "nickname": root.state.nickname,
            "target": target_group_name,
        },
        tags=GENERAL_TAG,
        subject=(
            f"Root moved from [{source_group_name}] to [{target_group_name}]"
        ),
        template_name="root_moved",
    )
    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
