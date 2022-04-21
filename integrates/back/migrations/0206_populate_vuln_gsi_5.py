# pylint: disable=invalid-name
"""
Populate the zero risk index in vulnerabilities.
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
    ZR_FILTER_STATUSES,
    ZR_INDEX_METADATA,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.utils import (
    format_vulnerability,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
    UnavailabilityError,
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


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    sleep_seconds=5,
)
async def populate_zr_index_by_vuln(current_item: Dict) -> None:
    key_structure = TABLE.primary_key
    gsi_5_index = TABLE.indexes["gsi_5"]
    vulnerability = format_vulnerability(current_item)
    gsi_5_key = keys.build_key(
        facet=ZR_INDEX_METADATA,
        values={
            "finding_id": vulnerability.finding_id,
            "vuln_id": vulnerability.id,
            "is_deleted": str(
                vulnerability.state.status is VulnerabilityStateStatus.DELETED
            ).lower(),
            "is_zero_risk": str(
                bool(
                    vulnerability.zero_risk
                    and vulnerability.zero_risk.status in ZR_FILTER_STATUSES
                )
            ).lower(),
            "state_status": str(vulnerability.state.status.value).lower(),
            "verification_status": str(
                vulnerability.verification
                and vulnerability.verification.status.value
            ).lower(),
        },
    )
    vulnerability_item = {
        gsi_5_index.primary_key.partition_key: gsi_5_key.partition_key,
        gsi_5_index.primary_key.sort_key: gsi_5_key.sort_key,
    }
    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "id": vulnerability.id,
        },
    )
    if current_item.get(
        gsi_5_index.primary_key.partition_key
    ) != vulnerability_item.get(
        gsi_5_index.primary_key.partition_key
    ) or current_item.get(
        gsi_5_index.primary_key.sort_key
    ) != vulnerability_item.get(
        gsi_5_index.primary_key.sort_key
    ):
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists()
            & (
                Attr(gsi_5_index.primary_key.sort_key).eq(
                    current_item.get(gsi_5_index.primary_key.sort_key, "")
                )
                | Attr(gsi_5_index.primary_key.sort_key).not_exists()
            ),
            item=vulnerability_item,
            key=vulnerability_key,
            table=TABLE,
        )


@retry_on_exceptions(
    exceptions=(ConditionalCheckFailedException,),
    sleep_seconds=5,
)
async def populate_zr_by_finding(finding: Finding) -> None:
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
            populate_zr_index_by_vuln(current_item=current_item)
            for current_item in response.items
        )
    )


@retry_on_exceptions(
    exceptions=(HTTPClientError,),
    sleep_seconds=5,
)
async def populate_zr_index_by_group(
    loaders: Dataloaders, group_name: str, progress: float
) -> None:
    all_findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    await collect(
        populate_zr_by_finding(finding=finding) for finding in all_findings
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
            populate_zr_index_by_group(
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
