from batch.dal import (
    get_actions_by_name,
    put_action,
    SkimsBatchQueue,
)
from batch.enums import (
    Action,
    Product,
)
from batch.types import (
    PutActionResult,
)
from custom_exceptions import (
    RootAlreadyCloning,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
import json
import logging
import logging.config
import os
from settings.logger import (
    LOGGING,
)
from typing import (
    Any,
    NamedTuple,
)


def _json_load(path: str) -> Any:
    with open(path, encoding="utf-8") as file:
        return json.load(file)


logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
QUEUES: dict[str, dict[str, str]] = _json_load(os.environ["MACHINE_QUEUES"])
FINDINGS: dict[str, dict[str, dict[str, str]]] = _json_load(
    os.environ["MACHINE_FINDINGS"]
)


class JobArguments(NamedTuple):
    group_name: str
    finding_code: str
    root_nickname: str


def _get_priority_suffix(urgent: bool) -> str:
    return "soon" if urgent else "later"


def get_queue_for_finding(finding_code: str, urgent: bool = False) -> str:
    for queue_ in QUEUES:
        if finding_code in QUEUES[queue_]["findings"]:
            return f"{queue_}_{_get_priority_suffix(urgent)}"

    raise NotImplementedError(f"{finding_code} does not belong to a queue")


def get_finding_code_from_title(finding_title: str) -> str | None:
    for finding_code in FINDINGS:
        for locale in FINDINGS[finding_code]:
            if finding_title == FINDINGS[finding_code][locale]["title"]:
                return finding_code
    return None


async def _queue_sync_git_roots(
    *,
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    roots: tuple[GitRoot, ...] | None = None,
    check_existing_jobs: bool = True,
    force: bool = False,
    queue_with_vpn: bool = False,
) -> PutActionResult | None:

    from roots import (  # pylint: disable=import-outside-toplevel
        domain as roots_domain,
    )

    try:
        return await roots_domain.queue_sync_git_roots(
            loaders=loaders,
            user_email=user_email,
            group_name=group_name,
            roots=roots,
            check_existing_jobs=check_existing_jobs,
            force=force,
            queue_with_vpn=queue_with_vpn,
        )
    except RootAlreadyCloning:
        current_jobs = sorted(
            await get_actions_by_name("clone_roots", group_name),
            key=lambda x: x.time,
        )
        if current_jobs:
            return PutActionResult(
                success=True,
                batch_job_id=current_jobs[0].batch_job_id,
                dynamo_pk=current_jobs[0].key,
            )
    return None


async def queue_job_new(  # pylint: disable=too-many-arguments
    group_name: str,
    dataloaders: Dataloaders,
    finding_codes: tuple[str, ...] | list[str],
    queue: SkimsBatchQueue = SkimsBatchQueue.SMALL,
    roots: tuple[str, ...] | list[str] | None = None,
    clone_before: bool = False,
    **kwargs: Any,
) -> PutActionResult | None:
    queue_result: PutActionResult | None = None
    group = await dataloaders.group.load(group_name)
    if (
        group
        and group.state.has_machine
        and group.state.managed != GroupManaged.UNDER_REVIEW
    ):
        group_roots = await dataloaders.group_roots.load(group_name)
        group_git_roots: list[GitRoot] = [
            root
            for root in group_roots
            if isinstance(root, GitRoot)
            and root.state.status == RootStatus.ACTIVE
        ]
        if not roots:
            roots = list(
                root.state.nickname
                for root in group_git_roots
                if (
                    (root.state.credential_id is not None and clone_before)
                    or not clone_before
                )
            )

        if roots:
            if (
                clone_before
                and (
                    result_clone := (
                        await _queue_sync_git_roots(
                            loaders=dataloaders,
                            user_email="integrates@fluidattacks.com",
                            group_name=group_name,
                            force=True,
                            roots=tuple(
                                root
                                for root in group_git_roots
                                if root.state.nickname in roots
                            ),
                        )
                    )
                )
                and (clone_job_id := result_clone.batch_job_id)
            ):
                kwargs["dependsOn"] = [
                    {"jobId": clone_job_id, "type": "SEQUENTIAL"},
                ]

            queue_result = await put_action(
                action=Action.EXECUTE_MACHINE,
                vcpus=2,
                product_name=Product.SKIMS,
                queue=queue,
                entity=group_name,
                additional_info=json.dumps(
                    {
                        "roots": list(sorted(roots)),
                        "checks": list(sorted(finding_codes)),
                    }
                ),
                attempt_duration_seconds=43200,
                subject="integrates@fluidattacks.com",
                memory=3700,
                **kwargs,
            )

    return queue_result


__all__ = [
    "SkimsBatchQueue",
]
