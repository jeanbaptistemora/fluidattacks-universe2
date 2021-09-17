from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from groups.domain import (
    get_active_groups,
    get_attributes,
)
from newutils.utils import (
    get_key_or_fallback,
)
import random
from schedulers.common import (
    info,
    machine_queue,
)
import skims_sdk
from typing import (
    List,
    Tuple,
)


async def main() -> None:
    groups: List[str] = await get_active_groups()
    dataloaders: Dataloaders = get_new_context()
    groups_data = await collect(
        get_attributes(group, ["historic_configuration"]) for group in groups
    )
    groups_confs = [
        group_data["historic_configuration"][-1] for group_data in groups_data
    ]

    info("Computing jobs")
    jobs: List[Tuple[str, str, str]] = [
        (group, check, root.state.nickname)
        for group, group_conf in zip(groups, groups_confs)
        if get_key_or_fallback(group_conf, "has_machine", "has_skims", False)
        for root in await dataloaders.group_roots.load(group)
        if root.state.status == "ACTIVE"
        for check in skims_sdk.FINDINGS
        if skims_sdk.is_check_available(check)
    ]
    random.shuffle(jobs)

    for group, check, namespace in jobs:
        info("%s-%s-%s", group, check, namespace)
        await machine_queue(
            finding_code=check,
            group_name=group,
            namespace=namespace,
            urgent=False,
        )
