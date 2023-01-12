from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
    IntegratesBatchQueue,
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
    RepeatedToePort,
    ToeInputAlreadyUpdated,
    ToeLinesAlreadyUpdated,
    ToePortAlreadyUpdated,
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
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingState,
)
from db_model.roots.types import (
    GitRoot,
    IPRoot,
    Root,
    URLRoot,
)
from db_model.stakeholders.types import (
    Stakeholder,
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
from db_model.toe_ports.types import (
    RootToePortsRequest,
    ToePort,
    ToePortRequest,
)
from db_model.utils import (
    get_datetime_with_offset,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from group_access import (
    domain as group_access_domain,
)
import itertools
import json
import logging
import logging.config
from mailer.common import (
    GENERAL_TAG,
    send_mails_async,
)
from operator import (
    attrgetter,
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
from toe.ports import (
    domain as toe_ports_domain,
)
from toe.ports.types import (
    ToePortAttributesToAdd,
    ToePortAttributesToUpdate,
)
from typing import (
    List,
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
LOGGER = logging.getLogger(__name__)


async def _process_vuln(
    *,
    loaders: Dataloaders,
    vuln: Vulnerability,
    target_finding_id: str,
    target_group_name: str,
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
    historic_state: tuple[
        VulnerabilityState, ...
    ] = await loaders.vulnerability_historic_state.load(vuln.id)
    historic_treatment: tuple[
        VulnerabilityTreatment, ...
    ] = await loaders.vulnerability_historic_treatment.load(vuln.id)
    historic_verification: tuple[
        VulnerabilityVerification, ...
    ] = await loaders.vulnerability_historic_verification.load(vuln.id)
    historic_zero_risk: tuple[
        VulnerabilityZeroRisk, ...
    ] = await loaders.vulnerability_historic_zero_risk.load(vuln.id)
    new_id = str(uuid.uuid4())
    await vulns_model.add(
        vulnerability=vuln._replace(
            finding_id=target_finding_id,
            group_name=target_group_name,
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
    new_vulnerability = await loaders.vulnerability.load(new_id)
    await vulns_model.update_historic(
        current_value=new_vulnerability,
        historic=historic_state or (vuln.state,),
    )
    if historic_treatment:
        loaders.vulnerability.clear(vuln.id)
        new_vulnerability = await loaders.vulnerability.load(new_id)
        await vulns_model.update_historic(
            current_value=new_vulnerability,
            historic=historic_treatment,
        )
    if historic_verification:
        loaders.vulnerability.clear(vuln.id)
        new_vulnerability = await loaders.vulnerability.load(new_id)
        await vulns_model.update_historic(
            current_value=new_vulnerability,
            historic=historic_verification,
        )
    if historic_zero_risk:
        loaders.vulnerability.clear(vuln.id)
        new_vulnerability = await loaders.vulnerability.load(new_id)
        await vulns_model.update_historic(
            current_value=new_vulnerability,
            historic=historic_zero_risk,
        )
    await vulns_domain.close_by_exclusion(
        vulnerability=vuln,
        modified_by=item_subject,
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
    vulns: tuple[Vulnerability, ...],
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
    target_group_findings: tuple[
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
        if source_finding.creation:
            initial_state = FindingState(
                modified_by=source_finding.hacker_email,
                modified_date=source_finding.creation.modified_date,
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
            submission_date = get_datetime_with_offset(
                initial_state.modified_date,
                source_finding.submission.modified_date,
            )
            await findings_model.update_state(
                current_value=initial_state,
                finding_id=target_finding_id,
                group_name=target_group_name,
                state=source_finding.submission._replace(
                    modified_date=submission_date
                ),
            )
            if source_finding.approval:
                approval_date = get_datetime_with_offset(
                    submission_date,
                    source_finding.approval.modified_date,
                )
                await findings_model.update_state(
                    current_value=source_finding.submission,
                    finding_id=target_finding_id,
                    group_name=target_group_name,
                    state=source_finding.approval._replace(
                        modified_date=approval_date
                    ),
                )

    target_vuln_ids = await collect(
        tuple(
            _process_vuln(
                loaders=loaders,
                vuln=vuln,
                target_finding_id=target_finding_id,
                target_group_name=target_group_name,
                target_root_id=target_root_id,
                item_subject=item_subject,
            )
            for vuln in vulns
            if vuln.state.status
            not in {
                VulnerabilityStateStatus.DELETED,
                VulnerabilityStateStatus.MASKED,
            }
            and (
                vuln.state.reasons is None
                or (
                    vuln.state.reasons
                    and VulnerabilityStateReason.EXCLUSION
                    not in vuln.state.reasons
                )
            )
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
            update_unreliable_indicators_by_deps(
                EntityDependency.move_root,
                finding_ids=[source_finding_id],
                vulnerability_ids=[vuln.id for vuln in vulns],
            ),
            update_unreliable_indicators_by_deps(
                EntityDependency.move_root,
                finding_ids=[target_finding_id],
                vulnerability_ids=target_vuln_ids,  # type: ignore
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
    if toe_input.state.seen_at is None:
        return
    attributes_to_add = ToeInputAttributesToAdd(
        attacked_at=toe_input.state.attacked_at,
        attacked_by=toe_input.state.attacked_by,
        be_present=False,
        first_attack_at=toe_input.state.first_attack_at,
        has_vulnerabilities=toe_input.state.has_vulnerabilities,
        seen_first_time_by=toe_input.state.seen_first_time_by,
        unreliable_root_id=target_root_id,
        seen_at=toe_input.state.seen_at,
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
            attacked_at=toe_input.state.attacked_at,
            attacked_by=toe_input.state.attacked_by,
            first_attack_at=toe_input.state.first_attack_at,
            has_vulnerabilities=toe_input.state.has_vulnerabilities,
            seen_at=toe_input.state.seen_at,
            seen_first_time_by=toe_input.state.seen_first_time_by,
            unreliable_root_id=target_root_id,
        )
        await toe_inputs_update(
            current_value=current_value,
            attributes=attributes_to_update,
            modified_by="machine@fluidattacks.com",
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
            loaders,
            target_group_name,
            target_root_id,
            toe_lines.filename,
            attributes_to_add,
            is_moving_toe_lines=True,
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


toe_ports_add = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_ports_domain.add)
toe_ports_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_ports_domain.update)


@retry_on_exceptions(
    exceptions=(ToePortAlreadyUpdated,),
)
async def _process_toe_port(
    loaders: Dataloaders,
    target_group_name: str,
    target_root_id: str,
    toe_port: ToePort,
    modified_by: str,
) -> None:
    if toe_port.seen_at is None:
        return
    attributes_to_add = ToePortAttributesToAdd(
        attacked_at=toe_port.state.attacked_at,
        attacked_by=toe_port.state.attacked_by,
        be_present=False,
        first_attack_at=toe_port.state.first_attack_at,
        has_vulnerabilities=toe_port.state.has_vulnerabilities,
        seen_first_time_by=toe_port.seen_first_time_by,
        seen_at=toe_port.seen_at,
    )
    try:
        await toe_ports_add(
            loaders,
            target_group_name,
            toe_port.address,
            toe_port.port,
            target_root_id,
            attributes_to_add,
            modified_by,
            is_moving_toe_port=True,
        )
    except RepeatedToePort:
        current_value: ToePort = await loaders.toe_port.load(
            ToePortRequest(
                address=toe_port.address,
                port=toe_port.port,
                group_name=toe_port.group_name,
                root_id=toe_port.root_id,
            )
        )
        attributes_to_update = ToePortAttributesToUpdate(
            attacked_at=toe_port.state.attacked_at,
            attacked_by=toe_port.state.attacked_by,
            first_attack_at=toe_port.state.first_attack_at,
            has_vulnerabilities=toe_port.state.has_vulnerabilities,
            seen_at=toe_port.seen_at,
            seen_first_time_by=toe_port.seen_first_time_by,
        )
        await toe_ports_update(
            current_value,
            attributes_to_update,
            modified_by,
            is_moving_toe_port=True,
        )


async def get_recipients(
    loaders: Dataloaders,
    email_to: List[str],
    source_group_name: str,
    target_group_name: str,
) -> List[str]:
    stakeholder: Stakeholder = await loaders.stakeholder.load(email_to[0])
    if (
        Notification.ROOT_UPDATE
        not in stakeholder.state.notifications_preferences.email
    ):
        email_to = []
    roles: set[str] = {
        "customer_manager",
        "user_manager",
    }
    source_group_emails = (
        await group_access_domain.get_stakeholders_email_by_preferences(
            loaders=loaders,
            group_name=source_group_name,
            notification=Notification.ROOT_UPDATE,
            roles=roles,
        )
    )
    email_to.extend(source_group_emails)
    target_group_emails = (
        await group_access_domain.get_stakeholders_email_by_preferences(
            loaders=loaders,
            group_name=target_group_name,
            notification=Notification.ROOT_UPDATE,
            roles=roles,
        )
    )
    email_to.extend(target_group_emails)

    return email_to


async def move_root(*, item: BatchProcessing) -> None:
    info = json.loads(item.additional_info)
    target_group_name = info["target_group_name"]
    target_root_id = info["target_root_id"]
    source_group_name = info["source_group_name"]
    source_root_id = info["source_root_id"]
    loaders: Dataloaders = get_new_context()

    LOGGER.info("Moving root", extra={"extra": info})
    root: Root = await loaders.root.load((source_group_name, source_root_id))
    root_vulnerabilities: tuple[
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
    target_root: Root = await loaders.root.load(
        (target_group_name, target_root_id)
    )
    if isinstance(root, (GitRoot, URLRoot)):
        LOGGER.info("Updating ToE inputs")
        group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
            GroupToeInputsRequest(group_name=source_group_name)
        )
        root_toe_inputs = tuple(
            toe_input
            for toe_input in group_toe_inputs
            if toe_input.state.unreliable_root_id == source_root_id
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
            queue=IntegratesBatchQueue.SMALL,
        )
    if isinstance(root, GitRoot):
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
            attempt_duration_seconds=7200,
            entity=target_group_name,
            subject=item.subject,
            additional_info=target_root.state.nickname,
            product_name=Product.INTEGRATES,
            queue=IntegratesBatchQueue.SMALL,
        )
    if isinstance(root, IPRoot):
        LOGGER.info("Updating ToE ports")
        await collect(
            tuple(
                _process_toe_port(
                    loaders,
                    target_group_name,
                    target_root_id,
                    toe_port,
                    item.subject,
                )
                for toe_port in await loaders.root_toe_ports.load_nodes(
                    RootToePortsRequest(
                        group_name=source_group_name, root_id=source_root_id
                    )
                )
            )
        )
        await put_action(
            action=Action.REFRESH_TOE_PORTS,
            entity=target_group_name,
            subject=item.subject,
            additional_info=target_root.state.nickname,
            product_name=Product.INTEGRATES,
            queue=IntegratesBatchQueue.SMALL,
        )
    LOGGER.info(
        "Notifying stakeholders",
        extra={
            "extra": {
                "subject": item.subject,
            }
        },
    )
    await send_mails_async(
        get_new_context(),
        email_to=await get_recipients(
            loaders, [item.subject], source_group_name, target_group_name
        ),
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
    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
    LOGGER.info("Task completed successfully.")
