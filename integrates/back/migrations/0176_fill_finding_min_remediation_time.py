# pylint: disable=invalid-name
"""
This migration adds the minTimeToRemediate attr to existing drafts and findings
based on the remediation_time data kept for each vuln in the vulnerabilities
yaml

If there's a drift between the data kept in the findings and in the yaml, this
migration can be rerun to keep everything in line

Execution Time:    2022-02-01 at 16:24:45 UTC-5
Finalization Time: 2022-02-01 at 16:26:31 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from db_model import (
    TABLE,
)
from decimal import (
    Decimal,
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
from dynamodb.types import (
    Item,
    PrimaryKey,
)
from groups import (
    dal as groups_dal,
)
from newutils.findings import (
    get_vulns_file,
)
import time
from typing import (
    Dict,
    List,
    Optional,
)


def get_mttr(title: str, finding_info: Dict) -> Optional[Decimal]:
    finding_code = title[:3]
    if (
        finding_code in finding_info
        and "remediation_time" in finding_info[finding_code]
    ):
        return Decimal(finding_info[finding_code]["remediation_time"])
    return None


async def process_finding(
    *,
    finding: Item,
    new_mttr: Optional[Decimal],
) -> None:
    await operations.update_item(
        item={"min_time_to_remediate": new_mttr},
        key=PrimaryKey(
            partition_key=finding["pk"],
            sort_key=finding["sk"],
        ),
        table=TABLE,
    )


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    sleep_seconds=10,
)
async def process_group(
    *,
    group_name: str,
    progress: float,
    finding_info: Dict,
) -> None:
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name},
    )
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["finding_metadata"],),
        filter_expression=Attr("min_time_to_remediate").not_exists(),
        index=index,
        table=TABLE,
    )
    group_findings: List[Item] = response.items
    await collect(
        tuple(
            process_finding(
                finding=finding,
                new_mttr=get_mttr(finding["title"], finding_info),
            )
            for finding in group_findings
            if "title" in finding
        ),
        workers=64,
    )
    print(
        f"Group updated: {group_name}. "
        f"Findings processed: {len(group_findings)}. "
        f"Progress: {round(progress*100, 4)}"
    )


async def main() -> None:
    finding_info = get_vulns_file()
    group_names = sorted(await groups_dal.get_active_groups())
    active_groups_len = len(group_names)
    print(f"Groups to process: {len(group_names)}")
    await collect(
        tuple(
            process_group(
                group_name=group_name,
                progress=count / active_groups_len,
                finding_info=finding_info,
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=16,
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
