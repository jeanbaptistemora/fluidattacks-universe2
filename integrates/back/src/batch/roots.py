from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    RepeatedToeLines,
    ToeLinesAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
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
    GitRootItem,
    RootItem,
)
from db_model.toe_lines.types import (
    RootToeLinesRequest,
    ToeLines,
    ToeLinesRequest,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb import (
    operations,
)
from dynamodb.exceptions import (
    UnavailabilityError,
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
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToAdd,
    ToeLinesAttributesToUpdate,
)
from typing import (
    Any,
    Dict,
    Optional,
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

toe_lines_add = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_lines_domain.add)
toe_lines_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_lines_domain.update)


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
        await findings_model.update_state(
            current_value=initial_state,
            finding_id=target_finding_id,
            group_name=target_group_name,
            state=source_finding.submission._replace(
                modified_date=datetime_utils.get_iso_date()
            ),
        )
        await findings_model.update_state(
            current_value=source_finding.submission,
            finding_id=target_finding_id,
            group_name=target_group_name,
            state=source_finding.approval._replace(
                modified_date=datetime_utils.get_iso_date()
            ),
        )

    await process_vulns(vulns, target_finding_id)
    await collect(
        (
            update_indicators(source_finding_id, source_group_name),
            update_indicators(target_finding_id, target_group_name),
        )
    )


@retry_on_exceptions(
    exceptions=(ToeLinesAlreadyUpdated,),
)
async def process_toe_lines(
    loaders: Dataloaders,
    target_group_name: str,
    target_root_id: str,
    toe_lines: ToeLines,
) -> None:
    attributes_to_add = ToeLinesAttributesToAdd(
        attacked_at=toe_lines.attacked_at,
        attacked_by=toe_lines.attacked_by,
        attacked_lines=toe_lines.attacked_lines,
        comments=toe_lines.comments,
        commit_author=toe_lines.commit_author,
        be_present=False,
        be_present_until=toe_lines.be_present_until,
        first_attack_at=toe_lines.first_attack_at,
        loc=toe_lines.loc,
        modified_commit=toe_lines.modified_commit,
        modified_date=toe_lines.modified_date,
        seen_at=toe_lines.seen_at,
        sorts_risk_level=toe_lines.sorts_risk_level,
    )
    try:
        await toe_lines_add(
            target_group_name,
            target_root_id,
            toe_lines.filename,
            attributes_to_add,
        )
    except RepeatedToeLines:
        current_value: ToeLines = await loaders.toe_lines.load(
            ToeLinesRequest(
                filename=toe_lines.filename,
                group_name=target_group_name,
                root_id=target_root_id,
            )
        )
        attacked_at = current_value.attacked_at or toe_lines.attacked_at
        attacked_by = current_value.attacked_by or toe_lines.attacked_by
        attacked_lines = (
            current_value.attacked_lines or toe_lines.attacked_lines
        )
        comments = current_value.comments or toe_lines.comments
        attributes_to_update = ToeLinesAttributesToUpdate(
            attacked_at=attacked_at,
            attacked_by=attacked_by,
            attacked_lines=attacked_lines,
            comments=comments,
            first_attack_at=toe_lines.first_attack_at,
            seen_at=toe_lines.seen_at,
            sorts_risk_level=toe_lines.sorts_risk_level,
        )
        await toe_lines_update(current_value, attributes_to_update)


async def move_root(*, item: BatchProcessing) -> None:
    target_root_id: Optional[str] = None
    try:
        target_group_name, target_root_id = item.entity.split("/")
    except ValueError:
        target_group_name = item.entity
    source_group_name, source_root_id = item.additional_info.split("/")
    loaders = get_new_context()
    root: RootItem = await loaders.root.load(
        (source_group_name, source_root_id)
    )
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
    if target_root_id and isinstance(root, GitRootItem):
        repo_toe_lines = await loaders.root_toe_lines.load_nodes(
            RootToeLinesRequest(
                group_name=source_group_name, root_id=source_root_id
            )
        )
        await collect(
            tuple(
                process_toe_lines(
                    loaders,
                    target_group_name,
                    target_root_id,
                    toe_lines,
                )
                for toe_lines in repo_toe_lines
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
