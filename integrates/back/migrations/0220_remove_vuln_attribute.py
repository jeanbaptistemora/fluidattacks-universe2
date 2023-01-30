# type: ignore

# pylint: disable=invalid-name
"""
Remove not longer in use `repo` attribute

Execution Time:    2022-05-26 at 03:01:21 UTC
Finalization Time: 2022-05-26 at 04:00:59 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from custom_exceptions import (
    VulnNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.roots.types import (
    Root,
    RootRequest,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER_CONSOLE = logging.getLogger("console")


async def update_vulnerability(
    *,
    finding_id: str,
    metadata: dict[str, str],
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id, "id": vulnerability_id},
    )

    vulnerability_item = {
        key: None if not value else value
        for key, value in metadata.items()
        if value is not None
    }
    if vulnerability_item:
        try:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=vulnerability_item,
                key=vulnerability_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise VulnNotFound() from ex


async def process_vulnerability(
    *,
    finding_id: str,
    group_name: str,
    loaders: Dataloaders,
    item: Item,
) -> None:
    if "repo" not in item:
        return

    root_id_pk: str = (
        str(item["pk_2"]).split("#")[1] if item["pk_2"] != "ROOT" else ""
    )
    root_id: str = item.get("root_id", "")
    repo: str = item["repo"]
    if not root_id or not root_id_pk:
        return

    root_by_pk: Root = await loaders.root.load(
        RootRequest(group_name, root_id_pk)
    )
    root_by_id: Root = root_by_pk
    if root_id:
        root_by_id = await loaders.root.load(RootRequest(group_name, root_id))

    LOGGER_CONSOLE.info(
        "Processing vulnerability",
        extra={
            "extra": {
                "vulnerability_id": str(item["pk"]).split("#")[1],
                "finding_id": finding_id,
                "repo": repo,
                "root_by_id": root_by_id.id,
                "root_by_pk": root_by_pk.id,
            }
        },
    )

    if repo in {root_by_id.state.nickname, root_by_pk.state.nickname}:
        await update_vulnerability(
            finding_id=finding_id,
            metadata={
                "repo": "",
            },
            vulnerability_id=str(item["pk"]).split("#")[1],
        )
        return

    historic_root_by_pk = await loaders.root_historic_states.load(root_id_pk)
    historic_root_by_id = historic_root_by_pk
    if root_id:
        historic_root_by_id = await loaders.root_historic_states.load(root_id)

    nicknames: set[str] = {state.nickname for state in historic_root_by_id}
    nicknames.update({state.nickname for state in historic_root_by_pk})

    if repo in nicknames:
        await update_vulnerability(
            finding_id=finding_id,
            metadata={
                "repo": "",
            },
            vulnerability_id=str(item["pk"]).split("#")[1],
        )
        return

    LOGGER_CONSOLE.info(
        "Failed to update vulnerability!",
        extra={
            "extra": {
                "group_name": group_name,
                "finding_id": finding_id,
                "vulnerability_id": str(item["pk"]).split("#")[1],
                "repo": repo,
                "root_by_id": root_by_id.id,
                "root_by_pk": root_by_pk.id,
            }
        },
    )


async def get_finding_vulns(
    *,
    finding_id: str,
) -> tuple[Item, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["vulnerability_metadata"],),
        table=TABLE,
        index=index,
    )

    return response.items


async def process_finding(
    *,
    finding_id: str,
    group_name: str,
    loaders: Dataloaders,
) -> None:
    vuln_items = await get_finding_vulns(finding_id=finding_id)
    await collect(
        tuple(
            process_vulnerability(
                finding_id=finding_id,
                group_name=group_name,
                item=item,
                loaders=loaders,
            )
            for item in vuln_items
        ),
        workers=8,
    )


async def process_group(
    *,
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    findings = await loaders.group_findings.load(group_name)
    await collect(
        tuple(
            process_finding(
                finding_id=finding_id, group_name=group_name, loaders=loaders
            )
            for finding_id in [finding.id for finding in findings]
        ),
        workers=8,
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    active_groups = await orgs_domain.get_all_active_groups(loaders)
    active_group_names = sorted([group.name for group in active_groups])
    LOGGER_CONSOLE.info(
        "Active groups",
        extra={"extra": {"groups_len": len(active_group_names)}},
    )

    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / len(active_group_names),
            )
            for count, group_name in enumerate(active_group_names)
        ),
        workers=4,
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
