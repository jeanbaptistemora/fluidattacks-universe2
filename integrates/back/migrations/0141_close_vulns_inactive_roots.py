# pylint: disable=invalid-name
"""
This migration closes vulnerabilities that belong to inactive roots

Execution Time:    2021-09-29 at 15:25:04 UTCUTC
Finalization Time: 2021-09-29 at 15:36:18 UTCUTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.get import (
    GroupRootsLoader,
)
from db_model.roots.types import (
    RootItem,
)
from groups import (
    domain as groups_domain,
)
from roots import (
    dal as roots_dal,
)
import time
from typing import (
    Any,
    Dict,
    Tuple,
)
from vulnerabilities import (
    dal as vulns_dal,
)


async def close_vuln(vuln: Dict[str, Any], root: RootItem) -> None:
    print(
        "Closing vuln",
        f"{root.group_name}/{vuln['finding_id']}/{vuln['UUID']}",
        "from inactive root",
        root.id,
    )
    await vulns_dal.update(
        vuln["finding_id"],
        vuln["UUID"],
        {
            "historic_state": [
                *vuln["historic_state"],
                {
                    **vuln["historic_state"][-1],
                    "state": "closed",
                    "justification": "EXCLUSION",
                },
            ]
        },
    )


async def get_vulns(
    root: RootItem,
) -> Tuple[RootItem, Tuple[Dict[str, Any], ...]]:
    loaders = get_new_context()
    vulns = await roots_dal.get_root_vulns(
        loaders=loaders,
        group_name=root.group_name,
        nickname=root.state.nickname,
    )
    return (root, vulns)


async def process_group(roots: Tuple[RootItem, ...]) -> None:
    active_root_nicknames = [
        root.state.nickname for root in roots if root.state.status == "ACTIVE"
    ]
    inactive_roots = [
        root
        for root in roots
        if root.state.status == "INACTIVE"
        if root.state.nickname not in active_root_nicknames
    ]

    inactive_root_vulns = await collect(
        [get_vulns(root) for root in inactive_roots]
    )
    await collect(
        [
            close_vuln(vuln, root)
            for (root, vulns) in inactive_root_vulns
            for vuln in vulns
            if vuln["historic_state"][-1]["state"] not in {"closed", "DELETED"}
            and vuln.get("historic_zero_risk", [{"status": ""}])[-1]["status"]
            != "CONFIRMED"
        ]
    )


async def main() -> None:
    groups = await groups_domain.get_active_groups()
    await collect(
        [
            process_group(group_roots)
            for group_roots in await GroupRootsLoader().load_many(groups)
        ]
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
