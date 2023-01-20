from aioextensions import (
    collect,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from machine.jobs import (
    FINDINGS,
    queue_job_new,
)
from organizations import (
    domain as orgs_domain,
)
from schedulers.common import (
    info,
)
from typing import (
    Dict,
    List,
    Tuple,
)


async def main() -> None:
    loaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)
    machine_groups: List[Group] = [
        group
        for group in groups
        if group.state.has_machine is True
        and group.state.managed in (GroupManaged.MANAGED, GroupManaged.TRIAL)
    ]
    groups_roots: Tuple[
        Tuple[Root, ...], ...
    ] = await loaders.group_roots.load_many(
        [group.name for group in machine_groups]
    )

    queue: Dict[str, List[str]] = {}
    for group, roots in zip(machine_groups, groups_roots):
        valid_roots: List[str] = [
            root.state.nickname
            for root in roots
            if (
                isinstance(root, GitRoot)
                and root.state.status == RootStatus.ACTIVE
                and root.cloning.status == GitCloningStatus.OK
            )
        ]
        if valid_roots:
            info(
                "Queueing %s roots for group %s: [%s]",
                len(valid_roots),
                group.name,
                ", ".join(valid_roots),
            )
            queue.update({group.name: valid_roots})
    finding_codes: List[str] = list(FINDINGS.keys())
    await collect(
        (
            queue_job_new(
                group_name=group_name,
                dataloaders=loaders,
                finding_codes=finding_codes,
                root=nicknames,
            )
            for group_name, nicknames in queue.items()
        ),
        workers=20,
    )
