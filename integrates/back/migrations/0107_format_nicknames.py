# pylint: disable=invalid-name
"""
This migration formats root nicknames to make them compliant with the new
validations

Execution Time:    2021-07-27 at 17:24:58 UTC-05
Finalization Time: 2021-07-27 at 17:29:07 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from dynamodb.types import (
    GitRootState,
    RootItem,
)
from groups.dal import (
    get_active_groups,
)
import re
from roots import (
    dal as roots_dal,
    domain as roots_domain,
)
import time
from urllib.parse import (
    unquote,
    urlparse,
)
from vulnerabilities import (
    dal as vulns_dal,
)


def format_nickname(root: RootItem) -> str:
    is_dummy = (
        root.state.nickname.lower() == f"git@gitlab.com:{root.group_name}"
    )
    is_url_query = "?" in root.state.nickname or "&" in root.state.nickname

    nickname = (
        urlparse(root.metadata.url).path.split("/")[-1]
        if is_url_query
        else root.metadata.url.split(":")[-1]
        if is_dummy
        else unquote(root.state.nickname).split("/")[-1]
    )

    return re.sub(r"(?![a-zA-Z_0-9-]).", "_", nickname.rstrip()[:128])


async def update_root(root: RootItem) -> None:
    new_nickname = format_nickname(root)
    print(
        {
            "group": root.group_name,
            "id": root.id,
            "old": root.state.nickname,
            "new": new_nickname,
        },
    )
    loaders = get_new_context()
    vulns = await roots_dal.get_root_vulns(
        loaders=loaders,
        group_name=root.group_name,
        nickname=root.state.nickname,
    )
    await collect(
        tuple(
            vulns_dal.update(
                vuln["finding_id"],
                vuln["UUID"],
                {"repo_nickname": new_nickname},
            )
            for vuln in vulns
        )
    )

    await roots_dal.update_root_state(
        group_name=root.group_name,
        root_id=root.id,
        state=GitRootState(
            environment_urls=root.state.environment_urls,
            environment=root.state.environment,
            gitignore=root.state.gitignore,
            includes_health_check=root.state.includes_health_check,
            modified_by=root.state.modified_by,
            modified_date=root.state.modified_date,
            nickname=new_nickname,
            other=root.state.other,
            reason=root.state.reason,
            status=root.state.status,
        ),
    )


async def update_group(group_name: str) -> None:
    roots = await roots_domain.get_roots(group_name=group_name)
    affected_roots = tuple(
        root
        for root in roots
        if not re.match(r"^[a-zA-Z_0-9-]{1,128}$", root.state.nickname)
    )

    if affected_roots:
        await collect(tuple(update_root(root) for root in affected_roots))


async def main() -> None:
    groups = await get_active_groups()
    await collect(tuple(update_group(group_name) for group_name in groups))


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
