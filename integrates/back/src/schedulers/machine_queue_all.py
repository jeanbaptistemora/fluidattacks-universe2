from dataloaders import (
    Dataloaders,
    get_new_context,
)
from groups.domain import (
    get_active_groups,
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

    info("Computing jobs")
    jobs: List[Tuple[str, str, str]] = [
        (group, check, root.nickname)
        for group in groups
        for root in await dataloaders.group_roots.load(group)
        if root.state == "ACTIVE"
        for check in skims_sdk.FINDINGS
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
