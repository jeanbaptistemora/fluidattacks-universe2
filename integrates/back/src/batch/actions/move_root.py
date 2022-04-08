from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    RepeatedToeInput,
    RepeatedToeLines,
    ToeInputAlreadyUpdated,
    ToeLinesAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    findings as findings_model,
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Notification,
    Source,
    StateRemovalJustification,
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
    URLRootItem,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
    ToeInputRequest,
)
from db_model.toe_lines.types import (
    RootToeLinesRequest,
    ToeLines,
    ToeLinesRequest,
)
from db_model.users.types import (
    User,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
import itertools
import json
import logging
import logging.config
from mailer.common import (
    GENERAL_TAG,
    send_mails_async,
)
from newutils import (
    datetime as datetime_utils,
)
from operator import (
    attrgetter,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from settings import (
    LOGGING,
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToAdd,
    ToeInputAttributesToUpdate,
)
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToAdd,
    ToeLinesAttributesToUpdate,
)
from typing import (
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

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger("console")


async def _update_indicators(
    finding_id: str, group_name: str, vuln_ids: Tuple[str, ...]
) -> None:
    await redis_del_by_deps(
        "upload_file", finding_id=finding_id, group_name=group_name
    )
    await update_unreliable_indicators_by_deps(
        EntityDependency.move_root,
        finding_ids=[finding_id],
        vulnerability_ids=list(vuln_ids),
    )


async def _process_vuln(
    *,
    loaders: Dataloaders,
    vuln: Vulnerability,
    target_finding_id: str,
    target_root_id: str,
    item_subject: str,
) -> str:
    LOGGER.info(
        "Processing vuln",
        extra={
            "extra": {
                "vuln_id": vuln.id,
                "target_finding_id": target_finding_id,
                "target_root_id": target_root_id,
            }
        },
    )
    state_loader = loaders.vulnerability_historic_state
    treatment_loader = loaders.vulnerability_historic_treatment
    verification_loader = loaders.vulnerability_historic_verification
    zero_risk_loader = loaders.vulnerability_historic_zero_risk
    historic_state = await state_loader.load(vuln.id)
    historic_treatment = await treatment_loader.load(vuln.id)
    historic_verification = await verification_loader.load(vuln.id)
    historic_zero_risk = await zero_risk_loader.load(vuln.id)
    new_id = str(uuid.uuid4())
    await vulns_model.add(
        vulnerability=vuln._replace(
            finding_id=target_finding_id,
            id=new_id,
            root_id=target_root_id,
            state=vuln.state,
        ),
    )
    LOGGER.info(
        "Created new vuln",
        extra={
            "extra": {
                "target_finding_id": target_finding_id,
                "new_id": new_id,
            }
        },
    )
    await vulns_model.update_historic(
        finding_id=target_finding_id,
        vulnerability_id=new_id,
        historic=historic_state or [vuln.state],
    )
    if historic_treatment:
        await vulns_model.update_historic(
            finding_id=target_finding_id,
            vulnerability_id=new_id,
            historic=historic_treatment,
        )
    if historic_verification:
        await vulns_model.update_historic(
            finding_id=target_finding_id,
            vulnerability_id=new_id,
            historic=historic_verification,
        )
    if historic_zero_risk:
        await vulns_model.update_historic(
            finding_id=target_finding_id,
            vulnerability_id=new_id,
            historic=historic_zero_risk,
        )
    await vulns_domain.close_by_exclusion(
        vulnerability=vuln,
        modified_by=item_subject,
        source=Source.ASM,
    )
    LOGGER.info(
        "Old vuln closed by exclusion",
        extra={
            "extra": {
                "finding_id": vuln.finding_id,
                "vuln_id": vuln.id,
            }
        },
    )
    return new_id


async def _process_finding(
    *,
    loaders: Dataloaders,
    source_group_name: str,
    target_group_name: str,
    target_root_id: str,
    source_finding_id: str,
    vulns: Tuple[Vulnerability, ...],
    item_subject: str,
) -> None:
    LOGGER.info(
        "Processing finding",
        extra={
            "extra": {
                "source_group_name": source_group_name,
                "target_group_name": target_group_name,
                "target_root_id": target_root_id,
                "source_finding_id": source_finding_id,
                "vulns": len(vulns),
            }
        },
    )
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
        LOGGER.info(
            "Found equivalent finding in target_group_findings",
            extra={
                "extra": {
                    "target_group_name": target_group_name,
                    "target_finding_id": target_finding_id,
                }
            },
        )
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
        LOGGER.info(
            "Equivalent finding not found. Created new one",
            extra={
                "extra": {
                    "target_group_name": target_group_name,
                    "target_finding_id": target_finding_id,
                }
            },
        )
        if source_finding.submission:
            target_submission = source_finding.submission._replace(
                modified_date=datetime_utils.get_iso_date()
            )
            await findings_model.update_state(
                current_value=initial_state,
                finding_id=target_finding_id,
                group_name=target_group_name,
                state=target_submission,
            )
            if source_finding.approval:
                target_approval = source_finding.approval._replace(
                    modified_date=datetime_utils.get_iso_date()
                )
                await findings_model.update_state(
                    current_value=target_submission,
                    finding_id=target_finding_id,
                    group_name=target_group_name,
                    state=target_approval,
                )

    target_vuln_ids = await collect(
        tuple(
            _process_vuln(
                loaders=loaders,
                vuln=vuln,
                target_finding_id=target_finding_id,
                target_root_id=target_root_id,
                item_subject=item_subject,
            )
            for vuln in vulns
            if vuln.state.status != VulnerabilityStateStatus.DELETED
            and vuln.state.justification != StateRemovalJustification.EXCLUSION
        ),
        workers=100,
    )
    LOGGER.info(
        "Updating finding indicators",
        extra={
            "extra": {
                "source_group_name": source_group_name,
                "source_finding_id": source_finding_id,
                "target_group_name": target_group_name,
                "target_finding_id": target_finding_id,
            }
        },
    )
    await collect(
        (
            _update_indicators(
                source_finding_id,
                source_group_name,
                tuple(vuln.id for vuln in vulns),
            ),
            _update_indicators(
                target_finding_id, target_group_name, target_vuln_ids
            ),
        )
    )


toe_inputs_add = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_inputs_domain.add)
toe_inputs_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_inputs_domain.update)


@retry_on_exceptions(
    exceptions=(ToeInputAlreadyUpdated,),
)
async def _process_toe_input(
    loaders: Dataloaders,
    target_group_name: str,
    target_root_id: str,
    toe_input: ToeInput,
) -> None:
    if toe_input.seen_at is None:
        return
    attributes_to_add = ToeInputAttributesToAdd(
        attacked_at=toe_input.attacked_at,
        attacked_by=toe_input.attacked_by,
        be_present=False,
        first_attack_at=toe_input.first_attack_at,
        has_vulnerabilities=toe_input.has_vulnerabilities,
        seen_first_time_by=toe_input.seen_first_time_by,
        unreliable_root_id=target_root_id,
        seen_at=toe_input.seen_at,
    )
    try:
        await toe_inputs_add(
            loaders,
            target_group_name,
            toe_input.component,
            toe_input.entry_point,
            attributes_to_add,
            is_moving_toe_input=True,
        )
    except RepeatedToeInput:
        current_value: ToeInput = await loaders.toe_input.load(
            ToeInputRequest(
                component=toe_input.component,
                entry_point=toe_input.entry_point,
                group_name=target_group_name,
                root_id=target_root_id,
            )
        )
        attributes_to_update = ToeInputAttributesToUpdate(
            attacked_at=toe_input.attacked_at,
            attacked_by=toe_input.attacked_by,
            first_attack_at=toe_input.first_attack_at,
            has_vulnerabilities=toe_input.has_vulnerabilities,
            seen_at=toe_input.seen_at,
            seen_first_time_by=toe_input.seen_first_time_by,
            unreliable_root_id=target_root_id,
        )
        await toe_inputs_update(
            current_value,
            attributes_to_update,
            is_moving_toe_input=True,
        )


toe_lines_add = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_lines_domain.add)
toe_lines_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_lines_domain.update)


@retry_on_exceptions(
    exceptions=(ToeLinesAlreadyUpdated,),
)
async def _process_toe_lines(
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
        last_author=toe_lines.last_author,
        be_present=False,
        be_present_until=toe_lines.be_present_until,
        first_attack_at=toe_lines.first_attack_at,
        has_vulnerabilities=toe_lines.has_vulnerabilities,
        loc=toe_lines.loc,
        last_commit=toe_lines.last_commit,
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
        attributes_to_update = ToeLinesAttributesToUpdate(
            attacked_at=toe_lines.attacked_at,
            attacked_by=toe_lines.attacked_by,
            attacked_lines=toe_lines.attacked_lines,
            comments=toe_lines.comments,
            first_attack_at=toe_lines.first_attack_at,
            has_vulnerabilities=toe_lines.has_vulnerabilities,
            seen_at=toe_lines.seen_at,
            sorts_risk_level=toe_lines.sorts_risk_level,
        )
        await toe_lines_update(
            current_value,
            attributes_to_update,
            is_moving_toe_lines=True,
        )


async def move_root(*, item: BatchProcessing) -> None:
    info = json.loads(item.additional_info)
    target_group_name = info["target_group_name"]
    target_root_id = info["target_root_id"]
    source_group_name = info["source_group_name"]
    source_root_id = info["source_root_id"]
    loaders: Dataloaders = get_new_context()

    LOGGER.info("Moving root", extra={"extra": info})
    root: RootItem = await loaders.root.load(
        (source_group_name, source_root_id)
    )
    root_vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.root_vulnerabilities.load(root.id)
    vulns_by_finding = itertools.groupby(
        sorted(root_vulnerabilities, key=attrgetter("finding_id")),
        key=attrgetter("finding_id"),
    )
    LOGGER.info(
        "Root content",
        extra={
            "extra": {
                "vulnerabilities": len(root_vulnerabilities),
            },
        },
    )
    await collect(
        tuple(
            _process_finding(
                loaders=loaders,
                source_group_name=source_group_name,
                target_group_name=target_group_name,
                target_root_id=target_root_id,
                source_finding_id=source_finding_id,
                vulns=tuple(vulns),
                item_subject=item.subject,
            )
            for source_finding_id, vulns in vulns_by_finding
        ),
        workers=10,
    )
    LOGGER.info("Moving completed")
    target_root: RootItem = await loaders.root.load(
        (target_group_name, target_root_id)
    )
    if isinstance(root, (GitRootItem, URLRootItem)):
        LOGGER.info("Updating ToE inputs")
        group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
            GroupToeInputsRequest(group_name=source_group_name)
        )
        root_toe_inputs = tuple(
            toe_input
            for toe_input in group_toe_inputs
            if toe_input.unreliable_root_id == source_root_id
        )
        await collect(
            tuple(
                _process_toe_input(
                    loaders,
                    target_group_name,
                    target_root_id,
                    toe_input,
                )
                for toe_input in root_toe_inputs
            )
        )
        await put_action(
            action=Action.REFRESH_TOE_INPUTS,
            entity=target_group_name,
            subject=item.subject,
            additional_info=target_root.state.nickname,
            product_name=Product.INTEGRATES,
        )
    if isinstance(root, GitRootItem):
        LOGGER.info("Updating ToE lines")
        repo_toe_lines = await loaders.root_toe_lines.load_nodes(
            RootToeLinesRequest(
                group_name=source_group_name, root_id=source_root_id
            )
        )
        await collect(
            tuple(
                _process_toe_lines(
                    loaders,
                    target_group_name,
                    target_root_id,
                    toe_lines,
                )
                for toe_lines in repo_toe_lines
            )
        )
        await put_action(
            action=Action.REFRESH_TOE_LINES,
            entity=target_group_name,
            subject=item.subject,
            additional_info=target_root.state.nickname,
            product_name=Product.INTEGRATES,
        )
    user: User = await loaders.user.load(item.subject)
    if Notification.ROOT_MOVED in user.notifications_preferences.email:
        LOGGER.info(
            "Notifying user",
            extra={
                "extra": {
                    "subject": item.subject,
                }
            },
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
                f"Root moved from [{source_group_name}] "
                f"to [{target_group_name}]"
            ),
            template_name="root_moved",
        )
    else:
        LOGGER.info(
            "User disabled this notification. Won't notify",
            extra={
                "extra": {
                    "subject": item.subject,
                }
            },
        )
    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
    LOGGER.info("Task completed successfully.")
