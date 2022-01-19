# pylint: disable=invalid-name
"""
Populate the email in gsi_3 in vulnerabilities.
"""

from aioextensions import (
    collect,
    run,
)
from authz.enforcer import (
    get_group_level_enforcer,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
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
from db_model.vulnerabilities.constants import (
    ASSIGNED_INDEX_METADATA,
)
from db_model.vulnerabilities.utils import (
    format_vulnerability,
    get_assigned,
)
from dynamodb import (
    keys,
    operations,
)
from groups.dal import (
    get_all as get_all_groups,
)
import logging
import logging.config
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
PROD = True


async def populate_index(*, current: Dict, group_name: str) -> None:
    key_structure = TABLE.primary_key
    gsi_3_index = TABLE.indexes["gsi_3"]
    finding_id = current["sk"].split("#")[1]
    vulnerability_id = current["pk"].split("#")[1]
    user_email: str = get_assigned(
        treatment=format_vulnerability(current).treatment
    )
    if user_email:
        enforcer = await get_group_level_enforcer(user_email, with_cache=False)
        if not enforcer(group_name, "valid_assigned"):
            user_email = ""
    gsi_3_key = keys.build_key(
        facet=ASSIGNED_INDEX_METADATA,
        values={
            "email": user_email,
            "vuln_id": vulnerability_id,
        },
    )
    vulnerability_item = {
        gsi_3_index.primary_key.partition_key: gsi_3_key.partition_key,
        gsi_3_index.primary_key.sort_key: gsi_3_key.sort_key,
    }

    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": finding_id,
            "id": vulnerability_id,
        },
    )
    if current.get(
        gsi_3_index.primary_key.partition_key
    ) != vulnerability_item.get(
        gsi_3_index.primary_key.partition_key
    ) or current.get(
        gsi_3_index.primary_key.sort_key
    ) != vulnerability_item.get(
        gsi_3_index.primary_key.sort_key
    ):
        LOGGER_CONSOLE.info(
            "Item is going to be updated!",
            extra={
                "extra": {
                    "vulnerability_item": vulnerability_item,
                    "gsi_3_index": gsi_3_index,
                    "vulnerability_key": vulnerability_key,
                }
            },
        )
        if PROD:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=vulnerability_item,
                key=vulnerability_key,
                table=TABLE,
            )


async def populate_by_finding(
    *,
    finding: Finding,
    group_name: str,
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
            populate_index(current=current_item, group_name=group_name)
            for current_item in response.items
        ),
        workers=32,
    )


async def populate_by_group(
    *,
    loaders: Dataloaders,
    group_name: str,
) -> None:
    LOGGER_CONSOLE.info(
        "Working on group",
        extra={
            "extra": {
                "group_name": group_name,
            }
        },
    )
    group_drafts_and_findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    group_removed_findings: Tuple[
        Finding, ...
    ] = await loaders.group_removed_findings.load(group_name)
    all_findings = group_drafts_and_findings + group_removed_findings
    await collect(
        tuple(
            populate_by_finding(finding=finding, group_name=group_name)
            for finding in all_findings
        ),
        workers=16,
    )


async def main() -> None:
    groups = await get_all_groups(data_attr="project_name")
    loaders = get_new_context()
    groups_names = list(
        sorted(set(str(group["project_name"]).lower() for group in groups))
    )
    await collect(
        tuple(
            populate_by_group(loaders=loaders, group_name=group_name)
            for group_name in groups_names
        ),
        workers=8,
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
