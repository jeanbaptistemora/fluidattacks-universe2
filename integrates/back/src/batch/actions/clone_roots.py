from aioextensions import (
    collect,
)
from batch.dal import (
    cancel_batch_job,
    delete_action,
    get_actions_by_name,
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
from batch.utils.git_self import (
    clone_root,
)
from batch.utils.s3 import (
    is_in_s3,
)
from custom_exceptions import (
    CredentialNotFound,
    InactiveRoot,
    InvalidParameter,
    RootAlreadyCloning,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.credentials.types import (
    CredentialItem,
)
from db_model.enums import (
    CredentialType,
)
from db_model.roots.types import (
    GitRootItem,
    RootItem,
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
import newutils.git
from newutils.git import (
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
    Set,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger("console")


async def clone_roots(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    root_nicknames: List[str] = item.additional_info.split(",")

    LOGGER.info(
        "Cloning roots for %s, %s",
        group_name,
        root_nicknames,
        extra={"extra": None},
    )

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

    LOGGER.info("%s roots will be cloned", len(roots), extra={"extra": None})
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

        LOGGER.info("Cloning %s", root.state.nickname, extra={"extra": None})
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
            extra=dict(extra=None),
        )
        if root_cloned.success and root_cloned.commit is not None:
            await roots_domain.update_root_cloning_status(
                loaders=dataloaders,
                group_name=group_name,
                root_id=root.id,
                status="OK",
                message="Cloned successfully",
                commit=root_cloned.commit,
                commit_date=root_cloned.commit_date,
            )
            cloned_roots_nicknames = (
                *cloned_roots_nicknames,
                root.state.nickname,
            )
        else:
            await roots_domain.update_root_cloning_status(
                loaders=dataloaders,
                group_name=group_name,
                root_id=root.id,
                status="FAILED",
                message="Clone failed",
            )

    findings = tuple(key for key in FINDINGS.keys() if is_check_available(key))
    if cloned_roots_nicknames:
        await queue_job_new(
            group_name=group_name,
            roots=cloned_roots_nicknames,
            finding_codes=findings,
            queue=SkimsBatchQueue.LOW,
        )
    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )


async def _ls_remote_root(
    root: RootItem, cred: CredentialItem
) -> Tuple[str, Optional[str]]:
    if cred.metadata.type == CredentialType.SSH:
        return (
            root.id,
            await ssh_ls_remote(
                repo_url=root.state.url, credential_key=cred.state.key
            ),
        )
    if cred.metadata.type == CredentialType.HTTPS:
        return (
            root.id,
            await newutils.git.https_ls_remote(
                repo_url=root.state.url,
                user=cred.state.user,
                password=cred.state.password,
                token=cred.state.token,
            ),
        )
    raise InvalidParameter()


async def queue_sync_git_roots(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    user_email: str,
    queue: str = "spot_soon",
    group_name: str,
    roots: Optional[Tuple[GitRootItem, ...]] = None,
    check_existing_jobs: bool = True,
    force: bool = False,
    queue_with_vpn: bool = False,
) -> Optional[PutActionResult]:
    current_jobs = sorted(
        await get_actions_by_name("clone_roots", group_name),
        key=lambda x: x.time,
    )
    roots = roots or await loaders.group_roots.load(group_name)
    roots = tuple(root for root in roots if root.state.status == "ACTIVE")
    roots_dict: Dict[str, GitRootItem] = {root.id: root for root in roots}

    if not roots:
        raise InactiveRoot()

    credentials_for_roots = {
        root_id: tuple(
            cred
            for cred in tuple(
                cred
                for cred in await loaders.group_credentials.load(group_name)
                if set(cred.state.roots).intersection(set(roots_dict.keys()))
            )
            if root_id in cred.state.roots
        )
        for root_id in roots_dict.keys()
    }
    credentials_for_roots = {
        root_id: creds[0]
        for root_id, creds in credentials_for_roots.items()
        if creds
    }

    if not credentials_for_roots:
        raise CredentialNotFound()

    roots_in_current_actions: Set[str] = set()
    current_action = None
    if current_jobs:
        LOGGER.info(
            "There are %s jobs in queue for %s",
            len(current_jobs),
            group_name,
            extra={"extra": None},
        )
        current_action = current_jobs[0]
        current_jobs = current_jobs[1:]
        roots_in_current_actions = {*current_action.additional_info.split(",")}

    for action in [item for item in current_jobs if not item.running]:
        roots_in_current_actions = {
            *roots_in_current_actions,
            *action.additional_info.split(","),
        }
        await delete_action(dynamodb_pk=action.key)
        if action.batch_job_id:
            LOGGER.info(
                "Canceling batch job %s for %s",
                action.batch_job_id,
                group_name,
                extra={"extra": None},
            )
            await cancel_batch_job(job_id=action.batch_job_id)

    if (
        check_existing_jobs
        and current_action
        and (
            not current_action.running
            and sorted(current_action.additional_info.split(","))
            == sorted(
                {
                    *[
                        roots_dict[root].state.nickname
                        for root in credentials_for_roots
                    ],
                    *roots_in_current_actions,
                }
            )
        )
    ):
        raise RootAlreadyCloning()

    last_commits_dict: Dict[str, Optional[str]] = dict(
        await collect(
            _ls_remote_root(roots_dict[root_id], cred)
            for root_id, cred in credentials_for_roots.items()
        )
    )

    await collect(
        [
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
                if not commit  # if the commite exists the credentials work
                and not roots_dict[root_id].state.use_vpn
            )
        ]
    )

    is_in_s3_dict = dict(
        await (
            collect(
                is_in_s3(group_name, root.state.nickname)
                for root in roots
                if root.id in credentials_for_roots
            )
        )
    )

    roots_to_clone = tuple(
        root_id
        for root_id in (
            root_id
            for root_id, commit in last_commits_dict.items()
            if (queue_with_vpn and roots_dict[root_id].state.use_vpn)
            or (
                commit  # if the commite exists the credentials work
                and (
                    force
                    or commit != roots_dict[root_id].cloning.commit
                    or not is_in_s3_dict.get(
                        roots_dict[root_id].state.nickname, False
                    )
                )
            )
        )
    )

    if roots_to_clone:
        result = await put_action(
            action=Action.CLONE_ROOTS,
            entity=group_name,
            subject=user_email,
            additional_info=",".join(
                {
                    *[
                        roots_dict[root_id].state.nickname
                        for root_id in set(roots_to_clone)
                    ],
                    *roots_in_current_actions,
                }
            ),
            queue=queue,
            product_name=Product.INTEGRATES,
            dynamodb_pk=current_action.key if current_action else None,
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
        return result
    return None
