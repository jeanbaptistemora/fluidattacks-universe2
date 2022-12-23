from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
    get_actions_by_name,
    IntegratesBatchQueue,
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from batch.types import (
    BatchProcessing,
    CloneResult,
    PutActionResult,
)
from batch_dispatch.utils.git_self import (
    clone_root,
)
from custom_exceptions import (
    CredentialNotFound,
    InvalidParameter,
    RootAlreadyCloning,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.events.types import (
    Event,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from events import (
    domain as events_domain,
)
from itertools import (
    chain,
)
import json
from json import (
    JSONDecodeError,
)
import logging
import logging.config
from machine.availability import (
    is_check_available,
)
from machine.jobs import (
    FINDINGS,
    queue_job_new,
    SkimsBatchQueue,
)
import newutils.git_self
from newutils.git_self import (
    ssh_ls_remote,
)
from roots import (
    domain as roots_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def clone_roots(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    root_nicknames: List[str] = []
    try:
        root_nicknames = json.loads(item.additional_info)["roots"]
    except JSONDecodeError:
        root_nicknames = item.additional_info.split(",")
    LOGGER.info(
        "Cloning roots for %s, %s",
        group_name,
        root_nicknames,
    )

    dataloaders: Dataloaders = get_new_context()
    group_roots_loader = dataloaders.group_roots
    group_roots = tuple(
        root
        for root in await group_roots_loader.load(group_name)
        if root.state.status == RootStatus.ACTIVE
    )
    group: Group = await dataloaders.group.load(group_name)

    # In the off case there are multiple roots with the same nickname
    root_ids = tuple(
        roots_domain.get_root_id_by_nickname(
            nickname=nickname,
            group_roots=group_roots,
            only_git_roots=True,
        )
        for nickname in root_nicknames
    )
    roots: Tuple[GitRoot, ...] = tuple(
        root for root in group_roots if root.id in root_ids
    )
    cloned_roots_nicknames: Tuple[str, ...] = tuple()

    LOGGER.info("%s roots will be cloned", len(roots))
    for root in roots:
        await roots_domain.update_root_cloning_status(
            loaders=dataloaders,
            group_name=group_name,
            root_id=root.id,
            status=GitCloningStatus.CLONING,
            message="Cloning in progress...",
        )
        root_cred: Optional[Credentials] = (
            await dataloaders.credentials.load(
                CredentialsRequest(
                    id=root.state.credential_id,
                    organization_id=group.organization_id,
                )
            )
            if root.state.credential_id
            else None
        )
        if not root_cred:
            LOGGER.error(
                "Root could not be determined or it"
                " does not have any credentials",
                extra=dict(extra=locals()),
            )
            continue
        root_cloned: CloneResult = CloneResult(success=False)

        LOGGER.info("Cloning %s", root.state.nickname)
        root_cloned = await clone_root(
            group_name=root.group_name,
            root_nickname=root.state.nickname,
            branch=root.state.branch,
            root_url=root.state.url,
            cred=root_cred,
        )
        LOGGER.info(
            "Cloned success: %s, with commit: %s",
            root_cloned.success,
            root_cloned.commit,
        )
        if root_cloned.success and root_cloned.commit is not None:
            await roots_domain.update_root_cloning_status(
                loaders=dataloaders,
                group_name=group_name,
                root_id=root.id,
                status=GitCloningStatus.OK,
                message="Cloned successfully",
                commit=root_cloned.commit,
                commit_date=root_cloned.commit_date,
            )
            LOGGER.info("Changed the status of %s", root.state.nickname)
            cloned_roots_nicknames = (
                *cloned_roots_nicknames,
                root.state.nickname,
            )
        else:
            await roots_domain.update_root_cloning_status(
                loaders=dataloaders,
                group_name=group_name,
                root_id=root.id,
                status=GitCloningStatus.FAILED,
                message=root_cloned.message
                if root_cloned.message and len(root_cloned.message) < 400
                else "Clone failed",
            )
            LOGGER.info("Failed to clone %s", root.state.nickname)

    findings = tuple(key for key in FINDINGS.keys() if is_check_available(key))

    if group.state.has_machine and cloned_roots_nicknames:
        queue = SkimsBatchQueue.MEDIUM
        await queue_job_new(
            dataloaders=dataloaders,
            group_name=group_name,
            roots=cloned_roots_nicknames,
            finding_codes=findings,
            queue=queue,
        )
    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )


async def _ls_remote_root(root: GitRoot, cred: Credentials) -> Optional[str]:
    last_commit: Optional[str]

    if root.state.use_vpn:
        last_commit = None
    elif isinstance(cred.state.secret, SshSecret):
        last_commit = await ssh_ls_remote(
            repo_url=root.state.url, credential_key=cred.state.secret.key
        )
    elif isinstance(cred.state.secret, HttpsSecret):
        last_commit = await newutils.git_self.https_ls_remote(
            repo_url=root.state.url,
            user=cred.state.secret.user,
            password=cred.state.secret.password,
        )
    elif isinstance(cred.state.secret, HttpsPatSecret):
        last_commit = await newutils.git_self.https_ls_remote(
            repo_url=root.state.url,
            token=cred.state.secret.token,
        )
    else:
        raise InvalidParameter()

    return last_commit


def _filter_active_roots_with_credentials(
    roots: Tuple[GitRoot, ...], use_vpn: bool
) -> Tuple[GitRoot, ...]:
    valid_roots: Tuple[GitRoot, ...] = tuple(
        root
        for root in roots
        if (
            root.state.status == RootStatus.ACTIVE
            and root.state.use_vpn == use_vpn
        )
    )
    if any(root.state.credential_id is None for root in roots):
        raise CredentialNotFound()

    return valid_roots


async def _filter_roots_unsolved_events(
    roots: Tuple[GitRoot, ...], loaders: Dataloaders, group_name: str
) -> Tuple[GitRoot, ...]:
    unsolved_events_by_root: Dict[
        str, Tuple[Event, ...]
    ] = await events_domain.get_unsolved_events_by_root(loaders, group_name)
    roots_with_unsolved_events: Tuple[str, ...] = tuple(
        root.id for root in roots if root.id in unsolved_events_by_root
    )
    await collect(
        [
            roots_domain.update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root_id,
                status=GitCloningStatus.FAILED,
                message="Git root has unsolved events",
            )
            for root_id in roots_with_unsolved_events
        ]
    )

    return tuple(
        root for root in roots if root.id not in roots_with_unsolved_events
    )


async def _filter_roots_already_in_queue(
    roots: Tuple[GitRoot, ...], group_name: str
) -> Tuple[GitRoot, ...]:
    clone_queue = await get_actions_by_name("clone_roots", group_name)
    root_nicknames_in_queue = set(
        chain.from_iterable(
            [clone_job.additional_info.split(",") for clone_job in clone_queue]
        )
    )
    valid_roots: Tuple[GitRoot, ...] = tuple(
        root
        for root in roots
        if root.state.nickname not in root_nicknames_in_queue
    )
    if not valid_roots:
        raise RootAlreadyCloning()

    return valid_roots


async def _filter_roots_working_creds(  # pylint: disable=too-many-arguments
    roots: Tuple[GitRoot, ...],
    loaders: Dataloaders,
    group_name: str,
    organization_id: str,
    force: bool,
    queue_with_vpn: bool,
) -> Tuple[GitRoot, ...]:
    roots_credentials: Tuple[
        Credentials, ...
    ] = await loaders.credentials.load_many(
        tuple(
            CredentialsRequest(
                id=root.state.credential_id,
                organization_id=organization_id,
            )
            for root in roots
            if root.state.credential_id is not None
        )
    )

    last_root_commits_in_s3: Tuple[
        Tuple[GitRoot, Optional[str], bool], ...
    ] = tuple(
        zip(
            roots,
            tuple(
                await collect(
                    _ls_remote_root(root, credential)
                    for root, credential in zip(roots, roots_credentials)
                )
            ),
            tuple(
                await collect(
                    roots_domain.is_in_s3(group_name, root.state.nickname)
                    for root in roots
                )
            ),
        )
    )

    roots_with_issues: Tuple[GitRoot, ...] = tuple(
        root
        for root, commit, _ in last_root_commits_in_s3
        if commit is None and not root.state.use_vpn
    )
    await collect(
        [
            roots_domain.update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root.id,
                status=GitCloningStatus.FAILED,
                message="Credentials does not work",
                commit=root.cloning.commit,
            )
            for root in roots_with_issues
        ]
    )

    unchanged_roots: Tuple[GitRoot, ...] = tuple(
        root
        for root, commit, has_mirror_in_s3 in last_root_commits_in_s3
        if (
            commit is not None
            and commit == root.cloning.commit
            and has_mirror_in_s3
            and force is False
        )
    )
    await collect(
        [
            roots_domain.update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root.id,
                status=root.cloning.status,
                message=root.cloning.reason,
                commit=root.cloning.commit,
            )
            for root in unchanged_roots
        ]
    )

    valid_roots = tuple(
        root
        for root, commit, has_mirror_in_s3 in last_root_commits_in_s3
        if (
            commit is not None
            and (
                commit != root.cloning.commit
                or not has_mirror_in_s3
                or force is True
            )
        )
        or (queue_with_vpn and root.state.use_vpn)
    )

    return valid_roots


async def queue_sync_git_roots(
    *,
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    roots: Optional[Tuple[GitRoot, ...]] = None,
    check_existing_jobs: bool = True,
    force: bool = False,
    queue_with_vpn: bool = False,
    from_scheduler: bool = False,
) -> Optional[PutActionResult]:
    group: Group = await loaders.group.load(group_name)
    if roots is None:
        roots = tuple(
            root
            for root in await loaders.group_roots.load(group_name)
            if (
                isinstance(root, GitRoot)
                and root.state.credential_id is not None
            )
        )
    valid_roots = _filter_active_roots_with_credentials(roots, queue_with_vpn)
    if not group.state.has_squad and not force:
        valid_roots = await _filter_roots_unsolved_events(
            valid_roots, loaders, group_name
        )

    if check_existing_jobs:
        valid_roots = await _filter_roots_already_in_queue(
            valid_roots, group_name
        )

    valid_roots = await _filter_roots_working_creds(
        valid_roots,
        loaders,
        group_name,
        group.organization_id,
        force,
        queue_with_vpn,
    )
    if valid_roots:
        additional_info = json.dumps(
            {
                "group_name": group_name,
                "roots": list({root.state.nickname for root in valid_roots}),
            }
        )
        result_clone = await put_action(
            action=Action.CLONE_ROOTS,
            attempt_duration_seconds=5400,
            vcpus=1,
            memory=1800,
            entity=group_name,
            subject=user_email,
            additional_info=additional_info,
            queue=IntegratesBatchQueue.CLONE,
            product_name=Product.INTEGRATES,
            dynamodb_pk=None,
        )
        if result_clone.batch_job_id:
            result_refresh = await put_action(
                action=Action.REFRESH_TOE_LINES,
                additional_info="*",
                attempt_duration_seconds=7200,
                entity=group_name,
                product_name=Product.INTEGRATES,
                subject="integrates@fluidattacks.com",
                queue=IntegratesBatchQueue.SMALL,
                dependsOn=[
                    {
                        "jobId": result_clone.batch_job_id,
                        "type": "SEQUENTIAL",
                    },
                ],
            )
            if result_refresh.batch_job_id:
                await put_action(
                    action=Action.REBASE,
                    additional_info=additional_info,
                    entity=group_name,
                    product_name=Product.INTEGRATES,
                    subject="integrates@fluidattacks.com",
                    queue=IntegratesBatchQueue.SMALL,
                    attempt_duration_seconds=14400,
                    dependsOn=[
                        {
                            "jobId": result_refresh.batch_job_id,
                            "type": "SEQUENTIAL",
                        },
                    ],
                )
        if not from_scheduler:
            await collect(
                tuple(
                    roots_domain.update_root_cloning_status(
                        loaders=loaders,
                        group_name=group_name,
                        root_id=root.id,
                        status=GitCloningStatus.QUEUED,
                        message="Cloning queued...",
                    )
                    for root in valid_roots
                )
            )

        return result_clone
    return None
