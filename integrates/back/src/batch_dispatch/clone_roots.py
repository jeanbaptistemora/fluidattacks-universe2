from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
    CloneResult,
)
from batch_dispatch.utils.git_self import (
    clone_root,
)
from dataloaders import (
    get_new_context,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
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
from roots import (
    domain as roots_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def clone_roots(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    root_nicknames: list[str] = []
    try:
        root_nicknames = json.loads(item.additional_info)["roots"]
    except JSONDecodeError:
        root_nicknames = item.additional_info.split(",")
    LOGGER.info(
        "Cloning roots for %s, %s",
        group_name,
        root_nicknames,
    )

    loaders = get_new_context()
    group_roots = tuple(
        root
        for root in await loaders.group_roots.load(group_name)
        if root.state.status == RootStatus.ACTIVE
    )
    group: Group = await loaders.group.load(group_name)

    # In the off case there are multiple roots with the same nickname
    root_ids = tuple(
        roots_domain.get_root_id_by_nickname(
            nickname=nickname,
            group_roots=group_roots,
            only_git_roots=True,
        )
        for nickname in root_nicknames
    )
    roots = tuple(
        root
        for root in group_roots
        if root.id in root_ids and isinstance(root, GitRoot)
    )
    cloned_roots_nicknames: tuple[str, ...] = tuple()

    LOGGER.info("%s roots will be cloned", len(roots))
    for root in roots:
        await roots_domain.update_root_cloning_status(
            loaders=loaders,
            group_name=group_name,
            root_id=root.id,
            status=GitCloningStatus.CLONING,
            message="Cloning in progress...",
        )
        root_cred: Optional[Credentials] = (
            await loaders.credentials.load(
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
            loaders=loaders,
        )
        LOGGER.info(
            "Cloned success: %s, with commit: %s",
            root_cloned.success,
            root_cloned.commit,
        )
        if root_cloned.success and root_cloned.commit is not None:
            await roots_domain.update_root_cloning_status(
                loaders=loaders,
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
                loaders=loaders,
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
        queue = SkimsBatchQueue.SMALL
        await queue_job_new(
            dataloaders=loaders,
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
