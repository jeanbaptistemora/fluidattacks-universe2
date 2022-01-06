# pylint: disable=invalid-name
"""
Populate the root_id and their gsi_2 in vulnerabilities.
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from botocore.exceptions import (
    HTTPClientError,
)
from custom_exceptions import (
    RootNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.types import (
    RootItem,
)
from db_model.vulnerabilities.constants import (
    ROOT_INDEX_METADATA,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from groups.dal import (
    get_all as get_all_groups,
)
import logging
import logging.config
from roots import (
    domain as roots_domain,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Dict,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    sleep_seconds=5,
)
async def populate_root_id_by_vuln(
    current_item: Dict, group_roots: Tuple[RootItem, ...]
) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    finding_id = current_item["sk"].split("#")[1]
    vulnerability_id = current_item["pk"].split("#")[1]
    is_root_found = True
    root_id = None
    try:
        root_id = (
            roots_domain.get_root_id_by_nickname(
                nickname=current_item["repo"],
                group_roots=group_roots,
                is_git_root=False,
            )
            if current_item.get("repo")
            else None
        )
    except RootNotFound:
        is_root_found = False
    gsi_2_key = keys.build_key(
        facet=ROOT_INDEX_METADATA,
        values={
            "root_id": "" if root_id is None else root_id,
            "vuln_id": vulnerability_id,
        },
    )
    vulnerability_item = {
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
    }
    if root_id is not None:
        vulnerability_item["root_id"] = root_id
    if not is_root_found:
        vulnerability_item["repo"] = None

    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": finding_id,
            "id": vulnerability_id,
        },
    )
    if (
        current_item.get(gsi_2_index.primary_key.partition_key)
        != vulnerability_item.get(gsi_2_index.primary_key.partition_key)
        or current_item.get(gsi_2_index.primary_key.sort_key)
        != vulnerability_item.get(gsi_2_index.primary_key.sort_key)
        or current_item.get("root_id") != vulnerability_item.get("root_id")
    ):
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )


async def populate_root_id_by_finding(
    finding: Finding, group_roots: Tuple[RootItem, ...]
) -> None:
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding.id},
    )
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["vulnerability_metadata"],),
        index=index,
        table=TABLE,
    )
    await collect(
        tuple(
            populate_root_id_by_vuln(
                current_item=current_item, group_roots=group_roots
            )
            for current_item in response.items
        )
    )


@retry_on_exceptions(
    exceptions=(HTTPClientError,),
    sleep_seconds=5,
)
async def populate_root_id_by_group(
    loaders: Dataloaders, group_name: str, progress: float
) -> None:
    group_roots: Tuple[RootItem, ...] = await loaders.group_roots.load(
        group_name
    )
    group_drafts_and_findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    group_removed_findings: Tuple[
        Finding, ...
    ] = await loaders.group_removed_findings.load(group_name)
    all_findings = group_drafts_and_findings + group_removed_findings
    await collect(
        populate_root_id_by_finding(finding=finding, group_roots=group_roots)
        for finding in all_findings
    )
    LOGGER_CONSOLE.info(
        "Group updated",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": str(progress),
            }
        },
    )


async def main() -> None:
    groups = await get_all_groups(data_attr="project_name")
    loaders = get_new_context()
    groups_len = len(groups)
    await collect(
        tuple(
            populate_root_id_by_group(
                loaders=loaders,
                group_name=group["project_name"],
                progress=count / groups_len,
            )
            for count, group in enumerate(groups)
        ),
        workers=5,
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
