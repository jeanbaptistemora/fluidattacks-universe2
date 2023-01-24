# pylint: disable=invalid-name
"""
Update existing findings of type F380, Supply Chain Attack - Docker,
so the description is updated with the latest changes in Criteria

Execution Time:    2022-10-05 at 21:47:13 UTC
Finalization Time: 2022-10-07 at 00:50:25 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingDescriptionToUpdate,
)
from newutils import (
    findings as findings_utils,
)
from organizations import (
    domain as orgs_domain,
)
import time
from typing import (
    Dict,
)


async def update_description(
    loaders: Dataloaders, group: Group, finding_id: str, criteria: Dict
) -> None:
    print(f"Updating F380 from group {group.name}")
    await findings_domain.update_description(
        loaders,
        finding_id,
        FindingDescriptionToUpdate(
            description=criteria["380"][group.language.value.lower()][
                "description"
            ]
        ),
    )


async def main() -> None:
    loaders = get_new_context()
    criteria = await findings_utils.get_vulns_file()
    groups = await orgs_domain.get_all_active_groups(loaders)
    groups_findings = await loaders.group_findings.load_many(
        [group.name for group in groups]
    )
    await collect(
        (
            update_description(loaders, group, finding.id, criteria)
            for group, findings in zip(groups, groups_findings)
            for finding in findings
            if finding.title.startswith("380")
        ),
        workers=15,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
