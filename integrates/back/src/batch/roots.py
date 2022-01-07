from aioextensions import (
    collect,
)
import asyncio
import base64
from batch.dal import (
    delete_action,
    put_action,
)
from batch.types import (
    BatchProcessing,
)
from context import (
    FI_AWS_S3_MIRRORS_BUCKET,
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
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingState,
)
from db_model.root_credentials.types import (
    RootCredentialItem,
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
from machine.availability import (
    is_check_available,
)
from machine.jobs import (
    FINDINGS,
    queue_all_checks_new,
    SkimsBatchQueue,
)
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
import os
from redis_cluster.operations import (
    redis_del_by_deps,
)
from roots import (
    domain as roots_domain,
)
from settings import (
    LOGGING,
)
import tempfile
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
from urllib.parse import (
    urlparse,
)
import uuid
from vulnerabilities import (
    dal as vulns_dal,
    domain as vulns_domain,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


toe_inputs_add = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_inputs_domain.add)
toe_inputs_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_inputs_domain.update)
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


async def process_vuln(
    *,
    loaders: Dataloaders,
    vuln: Vulnerability,
    target_finding_id: str,
    target_root_id: str,
    item_subject: str,
) -> None:
    state_loader = loaders.vulnerability_historic_state
    treatment_loader = loaders.vulnerability_historic_treatment
    verification_loader = loaders.vulnerability_historic_verification
    zero_risk_loader = loaders.vulnerability_historic_zero_risk
    historic_state = await state_loader.load(vuln.id)
    historic_treatment = await treatment_loader.load(vuln.id)
    historic_verification = await verification_loader.load(vuln.id)
    historic_zero_risk = await zero_risk_loader.load(vuln.id)
    new_id = str(uuid.uuid4())
    await vulns_dal.add(
        vulnerability=vuln._replace(
            finding_id=target_finding_id,
            id=new_id,
            root_id=target_root_id,
            state=vuln.state,
        ),
    )
    await vulns_dal.update_historic_state(
        finding_id=target_finding_id,
        vulnerability_id=new_id,
        historic_state=historic_state,
    )
    await vulns_dal.update_historic_treatment(
        finding_id=target_finding_id,
        vulnerability_id=new_id,
        historic_treatment=historic_treatment,
    )
    await vulns_dal.update_historic_verification(
        finding_id=target_finding_id,
        vulnerability_id=new_id,
        historic_verification=historic_verification,
    )
    await vulns_dal.update_historic_zero_risk(
        finding_id=target_finding_id,
        vulnerability_id=new_id,
        historic_zero_risk=historic_zero_risk,
    )
    await vulns_domain.close_by_exclusion(
        vulnerability=vuln,
        modified_by=item_subject,
        source=Source.ASM,
    )


async def process_finding(
    *,
    loaders: Dataloaders,
    source_group_name: str,
    target_group_name: str,
    target_root_id: str,
    source_finding_id: str,
    vulns: Tuple[Vulnerability, ...],
    item_subject: str,
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
        target_submission = source_finding.submission._replace(
            modified_date=datetime_utils.get_iso_date()
        )
        await findings_model.update_state(
            current_value=initial_state,
            finding_id=target_finding_id,
            group_name=target_group_name,
            state=target_submission,
        )
        target_approval = source_finding.approval._replace(
            modified_date=datetime_utils.get_iso_date()
        )
        await findings_model.update_state(
            current_value=target_submission,
            finding_id=target_finding_id,
            group_name=target_group_name,
            state=target_approval,
        )

    await collect(
        tuple(
            process_vuln(
                loaders=loaders,
                vuln=vuln,
                target_finding_id=target_finding_id,
                target_root_id=target_root_id,
                item_subject=item_subject,
            )
            for vuln in vulns
            if vuln.state.status != VulnerabilityStateStatus.DELETED
        ),
    )
    await collect(
        (
            update_indicators(source_finding_id, source_group_name),
            update_indicators(target_finding_id, target_group_name),
        )
    )


@retry_on_exceptions(
    exceptions=(ToeInputAlreadyUpdated,),
)
async def process_toe_input(
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
            target_group_name,
            toe_input.component,
            toe_input.entry_point,
            attributes_to_add,
        )
    except RepeatedToeInput:
        current_value: ToeInput = await loaders.toe_input.load(
            ToeInputRequest(
                component=toe_input.component,
                entry_point=toe_input.entry_point,
                group_name=target_group_name,
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
        await toe_inputs_update(current_value, attributes_to_update)


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
        has_vulnerabilities=toe_lines.has_vulnerabilities,
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
        attributes_to_update = ToeLinesAttributesToUpdate(
            attacked_at=toe_lines.attacked_at,
            attacked_by=toe_lines.attacked_by,
            attacked_lines=toe_lines.attacked_lines,
            comments=toe_lines.comments,
            first_attack_at=toe_lines.first_attack_at,
            has_vulnerabilities=toe_lines.has_vulnerabilities,
            seen_at=toe_lines.seen_at,
            sorts_risk_level=toe_lines.sorts_risk_level,
            is_moving_toe_lines=True,
        )
        await toe_lines_update(current_value, attributes_to_update)


async def move_root(*, item: BatchProcessing) -> None:
    target_group_name, target_root_id = item.entity.split("/")
    source_group_name, source_root_id = item.additional_info.split("/")
    loaders: Dataloaders = get_new_context()
    root: RootItem = await loaders.root.load(
        (source_group_name, source_root_id)
    )
    root_vulns = await loaders.root_vulns_typed.load(
        (source_group_name, root.state.nickname)
    )
    vulns_by_finding = tuple(
        itertools.groupby(
            sorted(root_vulns, key=attrgetter("finding_id")),
            key=attrgetter("finding_id"),
        )
    )
    await collect(
        tuple(
            process_finding(
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
    )
    target_root: RootItem = await loaders.root.load(
        (target_group_name, target_root_id)
    )
    if isinstance(root, (GitRootItem, URLRootItem)):
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
                process_toe_input(
                    loaders,
                    target_group_name,
                    target_root_id,
                    toe_input,
                )
                for toe_input in root_toe_inputs
            )
        )
        await put_action(
            action_name="refresh_toe_inputs",
            entity=target_group_name,
            subject=item.subject,
            additional_info=target_root.state.nickname,
        )
    if isinstance(root, GitRootItem):
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
        await put_action(
            action_name="refresh_toe_lines",
            entity=target_group_name,
            subject=item.subject,
            additional_info=target_root.state.nickname,
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


async def _upload_cloned_repo_to_s3(content_dir: str, group_name: str) -> bool:
    success: bool = False
    repo_path: str = os.path.join(content_dir, os.listdir(content_dir)[0])

    # Add metadata about the last cloning date, which is right now
    with open(
        os.path.join(repo_path, ".git/fluidattacks_metadata"),
        "w",
        encoding="utf-8",
    ) as metadata:
        json.dump(
            {
                "date": datetime_utils.convert_to_iso_str(
                    datetime_utils.get_now_as_str()
                )
            },
            metadata,
            indent=2,
        )

    # Create .keep files in empty directories so the structure is kept in S3
    empty_dirs = [
        root
        for root, dirs, files in os.walk(repo_path)
        if not dirs and not files
    ]
    for _dir in empty_dirs:
        with open(os.path.join(_dir, ".keep"), "w", encoding="utf-8"):
            pass

    proc = await asyncio.create_subprocess_exec(
        "aws",
        "s3",
        "sync",
        "--delete",
        "--sse",
        "AES256",
        "--exclude",
        "*",
        "--include",
        "*/.git/*",
        content_dir,
        f"s3://{FI_AWS_S3_MIRRORS_BUCKET}/{group_name}",
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        env={**os.environ.copy()},
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0 or stderr:
        LOGGER.error(
            "Uploading cloned root to S3 failed", extra=dict(extra=locals())
        )
    else:
        success = True
    return success


async def _ssh_clone_root(root: RootItem, cred: RootCredentialItem) -> bool:
    success: bool = False
    group_name: str = root.group_name
    root_url: str = root.state.url
    parsed_url = urlparse(root_url)
    raw_root_url = root_url.replace(f"{parsed_url.scheme}://", "")
    branch: str = root.state.branch
    with tempfile.TemporaryDirectory() as temp_dir:
        ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
        with open(
            os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
            "w",
            encoding="utf-8",
        ) as ssh_file:
            ssh_file.write(base64.b64decode(cred.state.key).decode())

        os.chdir(temp_dir)
        proc = await asyncio.create_subprocess_exec(
            "git",
            "clone",
            "--branch",
            branch,
            raw_root_url,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            env={
                **os.environ.copy(),
                "GIT_SSH_COMMAND": f"ssh -i {ssh_file_name}",
            },
        )
        _, stderr = await proc.communicate()

        os.remove(ssh_file_name)
        if proc.returncode != 0 or stderr:
            LOGGER.error("Root SSH cloning failed", extra=dict(extra=locals()))
        else:
            success = await _upload_cloned_repo_to_s3(temp_dir, group_name)
    return success


async def clone_root(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    root_nickname: str = item.additional_info

    dataloaders: Dataloaders = get_new_context()
    group_root_creds_loader = dataloaders.group_root_credentials
    group_roots_loader = dataloaders.group_roots
    group_creds = await group_root_creds_loader.load(group_name)
    group_roots = await group_roots_loader.load(group_name)

    # In the off case there are multiple roots with the same nickname
    root_id = roots_domain.get_root_id_by_nickname(
        nickname=root_nickname, group_roots=group_roots, is_git_root=True
    )
    root: RootItem = next(filter(lambda x: x.id == root_id, group_roots), None)
    root_cred: RootCredentialItem = next(
        filter(lambda x: root_nickname in x.state.roots, group_creds), None
    )

    root_cloned: bool = False
    if root and root_cred:
        if root_cred.metadata.type.value == "SSH":
            root_cloned = await _ssh_clone_root(root, root_cred)
    else:
        LOGGER.error(
            "Root could not be determined or it does not have any credentials",
            extra=dict(extra=locals()),
        )
    if root_cloned:
        findings = tuple(
            key for key in FINDINGS.keys() if is_check_available(key)
        )
        await queue_all_checks_new(
            group=group_name,
            roots=tuple(root.state.nickname),
            finding_codes=findings,
            queue=SkimsBatchQueue.HIGH,
        )
    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
