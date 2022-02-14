from aioextensions import (
    collect,
)
import asyncio
import base64
from batch.dal import (
    delete_action,
    get_actions_by_name,
    put_action,
)
from batch.types import (
    BatchProcessing,
    CloneResult,
)
from context import (
    FI_AWS_S3_MIRRORS_BUCKET,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    CredentialNotFound,
    InactiveRoot,
    RepeatedToeInput,
    RepeatedToeLines,
    RootAlreadyCloning,
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
from db_model.credentials.types import (
    CredentialItem,
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
import git
from git.exc import (
    GitError,
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
    Dict,
    List,
    Optional,
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


async def update_indicators(
    finding_id: str, group_name: str, vuln_ids: Tuple[str, ...]
) -> None:
    await redis_del_by_deps(
        "upload_file", finding_id=finding_id, group_name=group_name
    )
    await update_unreliable_indicators_by_deps(
        EntityDependency.move_root,
        finding_ids=[finding_id],
        vulnerability_ids=vuln_ids,
    )


async def process_vuln(
    *,
    loaders: Dataloaders,
    vuln: Vulnerability,
    target_finding_id: str,
    target_root_id: str,
    item_subject: str,
) -> str:
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
    if historic_treatment:
        await vulns_dal.update_historic_treatment(
            finding_id=target_finding_id,
            vulnerability_id=new_id,
            historic_treatment=historic_treatment,
        )
    if historic_verification:
        await vulns_dal.update_historic_verification(
            finding_id=target_finding_id,
            vulnerability_id=new_id,
            historic_verification=historic_verification,
        )
    if historic_zero_risk:
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
    return new_id


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
            update_indicators(
                source_finding_id,
                source_group_name,
                tuple(vuln.id for vuln in vulns),
            ),
            update_indicators(
                target_finding_id, target_group_name, target_vuln_ids
            ),
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
        is_moving_toe_input=True,
    )
    try:
        await toe_inputs_add(
            loaders,
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
            is_moving_toe_input=True,
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
    root_vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.root_vulnerabilities.load(root.id)
    vulns_by_finding = itertools.groupby(
        sorted(root_vulnerabilities, key=attrgetter("finding_id")),
        key=attrgetter("finding_id"),
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


async def _upload_cloned_repo_to_s3(
    *,
    repo_path: str,
    group_name: str,
    nickname: str,
) -> bool:
    success: bool = False

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
        with open(os.path.join(_dir, ".keep"), "w", encoding="utf-8") as file:
            file.close()

    proc = await asyncio.create_subprocess_exec(
        "aws",
        "s3",
        "sync",
        "--delete",
        "--sse",
        "AES256",
        "--exclude",
        f"{repo_path}/*",
        "--include",
        f"{repo_path}/.git/*",
        repo_path,
        f"s3://{FI_AWS_S3_MIRRORS_BUCKET}/{group_name}/{nickname}/",
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        env={**os.environ.copy()},
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        LOGGER.error(
            "Uploading root to S3 failed with error: %s",
            stderr.decode(),
            extra=dict(extra=locals()),
        )
    else:
        success = True
    return success


async def ssh_ls_remote_root(
    root: RootItem, cred: CredentialItem
) -> Optional[str]:
    root_url: str = root.state.url
    parsed_url = urlparse(root_url)
    raw_root_url = root_url.replace(f"{parsed_url.scheme}://", "")
    with tempfile.TemporaryDirectory() as temp_dir:
        ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
        with open(
            os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
            "w",
            encoding="utf-8",
        ) as ssh_file:
            ssh_file.write(base64.b64decode(cred.state.key).decode())

        proc = await asyncio.create_subprocess_exec(
            "git",
            "ls-remote",
            "-h",
            raw_root_url,
            root.state.branch,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            env={
                **os.environ.copy(),
                "GIT_SSH_COMMAND": (
                    f"ssh -i {ssh_file_name} -o"
                    "UserKnownHostsFile=/dev/null -o "
                    "StrictHostKeyChecking=no"
                ),
            },
        )
        stdout, _ = await proc.communicate()

        os.remove(ssh_file_name)

        if proc.returncode != 0:
            return None

        return stdout.decode().split("\t")[0]


async def ssh_clone_root(root: RootItem, cred: CredentialItem) -> CloneResult:
    success: bool = False
    group_name: str = root.group_name
    root_url: str = root.state.url
    raw_root_url = root_url.replace(f"{urlparse(root_url).scheme}://", "")
    branch: str = root.state.branch
    with tempfile.TemporaryDirectory() as temp_dir:
        ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
        with open(
            os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
            "w",
            encoding="utf-8",
        ) as ssh_file:
            ssh_file.write(base64.b64decode(cred.state.key).decode())

        folder_to_clone_root = f"{temp_dir}/{root.state.nickname}"
        proc = await asyncio.create_subprocess_exec(
            "git",
            "clone",
            "--branch",
            branch,
            raw_root_url,
            folder_to_clone_root,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            env={
                **os.environ.copy(),
                "GIT_SSH_COMMAND": (
                    f"ssh -i {ssh_file_name} -o"
                    "UserKnownHostsFile=/dev/null -o "
                    "StrictHostKeyChecking=no"
                ),
            },
        )
        _, stderr = await proc.communicate()

        os.remove(ssh_file_name)
        commit: Optional[str] = None
        if proc.returncode != 0:
            LOGGER.error(
                "Root SSH cloning failed with error: %s",
                stderr.decode(),
                extra=dict(extra=locals()),
            )
        else:
            success = await _upload_cloned_repo_to_s3(
                repo_path=folder_to_clone_root,
                group_name=group_name,
                nickname=root.state.nickname,
            )
            with suppress(GitError, AttributeError):
                commit = git.Repo(
                    folder_to_clone_root, search_parent_directories=True
                ).head.object.hexsha
    return CloneResult(success=success, commit=commit)


async def clone_roots(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    root_nicknames: List[str] = item.additional_info.split(",")

    dataloaders: Dataloaders = get_new_context()
    group_root_creds_loader = dataloaders.group_credentials
    group_roots_loader = dataloaders.group_roots
    group_creds = await group_root_creds_loader.load(group_name)
    group_roots = await group_roots_loader.load(group_name)

    # In the off case there are multiple roots with the same nickname
    root_ids = tuple(
        roots_domain.get_root_id_by_nickname(
            nickname=nickname,
            group_roots=group_roots,
            only_git_roots=True,
        )
        for nickname in root_nicknames
    )
    roots: Tuple[RootItem, ...] = tuple(
        root for root in group_roots if root.id in root_ids
    )
    cloned_roots_nicknames: Tuple[str, ...] = tuple()
    for root in roots:
        root_cred: Optional[CredentialItem] = next(
            (cred for cred in group_creds if root.id in cred.state.roots), None
        )
        if not root_cred:
            LOGGER.error(
                (
                    "Root could not be determined or it"
                    " does not have any credentials"
                ),
                extra=dict(extra=locals()),
            )
            continue
        root_cloned: CloneResult = CloneResult(success=False)

        if root_cred.metadata.type.value == "SSH":
            root_cloned = await ssh_clone_root(root, root_cred)
        if root_cloned.success:
            await roots_domain.update_root_cloning_status(
                loaders=dataloaders,
                group_name=group_name,
                root_id=root.id,
                status="OK" if root_cloned else "FAILED",
                message="Cloned successfully"
                if root_cloned
                else "Clone failed",
                commit=root_cloned.commit,
            )
            cloned_roots_nicknames = (
                *cloned_roots_nicknames,
                root.state.nickname,
            )

    findings = tuple(key for key in FINDINGS.keys() if is_check_available(key))
    if cloned_roots_nicknames:
        await queue_all_checks_new(
            group=group_name,
            roots=cloned_roots_nicknames,
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


async def _ssh_ls_remote_root(
    root: RootItem, cred: CredentialItem
) -> Tuple[str, Optional[str]]:
    return (root.id, await ssh_ls_remote_root(root, cred))


async def queue_sync_git_roots(
    *,
    loaders: Dataloaders,
    user_email: str,
    queue: str = "spot_soon",
    group_name: str,
    roots: Optional[Tuple[GitRootItem, ...]] = None,
    check_existing_jobs: bool = True,
) -> bool:
    if check_existing_jobs and (
        len(
            [
                action
                for action in await get_actions_by_name(
                    "clone_roots", group_name
                )
                # Check duplicated job at the group level (all roots)
                if (roots is None and action.entity == group_name)
                # Check duplicated job at the root level (selected roots)
                or (
                    roots is not None
                    and sorted(action.additional_info.split(","))
                    == sorted([root.state.nickname for root in roots])
                )
            ]
        )
        > 0
    ):
        raise RootAlreadyCloning()

    roots = roots or await loaders.group_roots.load(group_name)
    roots = tuple(root for root in roots if root.state.status == "ACTIVE")
    roots_dict: Dict[str, GitRootItem] = {root.id: root for root in roots}

    if not roots:
        raise InactiveRoot()

    group_creds: Tuple[
        CredentialItem, ...
    ] = await loaders.group_credentials.load(group_name)
    roots_cred: Tuple[CredentialItem, ...] = tuple(
        cred
        for cred in group_creds
        if set(cred.state.roots).intersection(set(roots_dict.keys()))
    )

    creds_by_root = {
        root_id: tuple(
            cred for cred in roots_cred if root_id in cred.state.roots
        )
        for root_id in roots_dict.keys()
    }
    creds_by_root = {
        root_id: creds[0]
        for root_id, creds in creds_by_root.items()
        if creds and creds[0].metadata.type.value == "SSH"
    }

    if not creds_by_root:
        raise CredentialNotFound()

    last_commits_dict = dict(
        await collect(
            _ssh_ls_remote_root(roots_dict[root_id], cred)
            for root_id, cred in creds_by_root.items()
        )
    )

    await collect(
        roots_domain.update_root_cloning_status(
            loaders=loaders,
            group_name=group_name,
            root_id=root_id,
            status="FAILED",
            message="Credentials does not work",
            commit=roots_dict[root_id].cloning.commit,
        )
        for root_id in (
            root_id
            for root_id, commit in last_commits_dict.items()
            if not commit
        )
    )
    await collect(
        roots_domain.update_root_cloning_status(
            loaders=loaders,
            group_name=group_name,
            root_id=root_id,
            status="OK",
            message="Already up to date",
            commit=roots_dict[root_id].cloning.commit,
        )
        for root_id in (
            root_id
            for root_id, commit in last_commits_dict.items()
            if commit and commit == roots_dict[root_id].cloning.commit
        )
    )

    roots_to_clone = tuple(
        root_id
        for root_id in (
            root_id
            for root_id, commit in last_commits_dict.items()
            if commit and commit != roots_dict[root_id].cloning.commit
        )
    )

    success: bool = False
    if roots_to_clone:
        await put_action(
            action_name="clone_roots",
            entity=group_name,
            subject=user_email,
            additional_info=",".join(
                roots_dict[root_id].state.nickname
                for root_id in roots_to_clone
            ),
            queue=queue,
        )
        await collect(
            roots_domain.update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root_id,
                status="CLONING",
                message="Cloning in progress...",
            )
            for root_id in roots_to_clone
        )
        success = True
    return success
