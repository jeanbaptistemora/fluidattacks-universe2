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
    Credential,
    CredentialRequest,
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from db_model.enums import (
    GitCloningStatus,
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
    cast,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def clone_roots(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    root_nicknames: List[str] = item.additional_info.split(",")

    LOGGER.info(
        "Cloning roots for %s, %s",
        group_name,
        root_nicknames,
    )

    dataloaders: Dataloaders = get_new_context()
    group_roots_loader = dataloaders.group_roots
    group_roots = await group_roots_loader.load(group_name)
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
        root_cred: Optional[Credential] = (
            await dataloaders.credential_new.load(
                CredentialRequest(
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
                message=root_cloned.message or "Clone failed",
            )
            LOGGER.info("Failed to clone %s", root.state.nickname)

    findings = tuple(key for key in FINDINGS.keys() if is_check_available(key))
    if cloned_roots_nicknames:
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


async def _ls_remote_root(
    root: GitRoot, cred: Credential, use_vpn: bool = False
) -> Tuple[str, Optional[str]]:
    if use_vpn:
        return (root.id, None)

    if isinstance(cred.state.secret, SshSecret):
        return (
            root.id,
            await ssh_ls_remote(
                repo_url=root.state.url, credential_key=cred.state.secret.key
            ),
        )
    if isinstance(cred.state.secret, HttpsSecret):
        return (
            root.id,
            await newutils.git.https_ls_remote(
                repo_url=root.state.url,
                user=cred.state.secret.user,
                password=cred.state.secret.password,
            ),
        )
    if isinstance(cred.state.secret, HttpsPatSecret):
        return (
            root.id,
            await newutils.git.https_ls_remote(
                repo_url=root.state.url,
                token=cred.state.secret.token,
            ),
        )
    raise InvalidParameter()


async def cancel_current_jobs(
    *,
    group_name: str,
) -> Set[str]:
    roots_in_current_actions: Set[str] = set()
    current_jobs = sorted(
        await get_actions_by_name("clone_roots", group_name),
        key=lambda x: x.time,
    )
    if current_jobs:
        LOGGER.info(
            "There are %s jobs in queue for %s",
            len(current_jobs),
            group_name,
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
            )
            await cancel_batch_job(job_id=action.batch_job_id)

    return roots_in_current_actions


async def queue_sync_git_roots(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    roots: Optional[Tuple[GitRoot, ...]] = None,
    check_existing_jobs: bool = True,
    force: bool = False,
    queue_with_vpn: bool = False,
) -> Optional[PutActionResult]:
    group: Group = await loaders.group.load(group_name)
    roots_in_current_actions: Set[str] = set()
    roots = roots or await loaders.group_roots.load(group_name)
    roots = tuple(
        root
        for root in roots
        if root.state.status == RootStatus.ACTIVE
        if isinstance(root, GitRoot)
        and (root.state.use_vpn if queue_with_vpn else True)
    )
    for root in roots:
        if root.state.credential_id is None:
            raise CredentialNotFound()

    roots_dict: Dict[str, GitRoot] = {root.id: root for root in roots}

    if not roots:
        raise InactiveRoot()

    root_credentials = cast(
        tuple[Credential, ...],
        await loaders.credential_new.load_many(
            tuple(
                CredentialRequest(
                    id=credential_id,
                    organization_id=group.organization_id,
                )
                for credential_id in {
                    root.state.credential_id
                    for root in roots
                    if root.state.credential_id is not None
                }
            )
        ),
    )
    root_credentials_dict: dict[str, Credential] = {
        credential.id: credential for credential in root_credentials
    }
    credentials_for_roots: dict[str, Credential] = {
        root.id: root_credentials_dict[root.state.credential_id]
        for root in roots
        if root.state.credential_id is not None
    }

    current_action: Optional[BatchProcessing] = None
    roots_in_current_actions = await cancel_current_jobs(group_name=group_name)

    if current_actions := sorted(
        await get_actions_by_name("clone_roots", group_name),
        key=lambda x: x.time,
    ):
        current_action = current_actions[0]

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
            _ls_remote_root(
                roots_dict[root_id], cred, roots_dict[root_id].state.use_vpn
            )
            for root_id, cred in credentials_for_roots.items()
        )
    )

    await collect(
        [
            roots_domain.update_root_cloning_status(
                loaders=loaders,
                group_name=group_name,
                root_id=root_id,
                status=GitCloningStatus.FAILED,
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
            vcpus=1,
            memory=1800,
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
            queue="clone",
            product_name=Product.INTEGRATES,
            dynamodb_pk=current_action.key if current_action else None,
        )

        return result
    return None
