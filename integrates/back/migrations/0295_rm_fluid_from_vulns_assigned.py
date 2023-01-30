# pylint: disable=invalid-name
"""
Remove fluid staff from treatment assignment in groups outside
`mura` and `imamura`.

Execution Time:    2022-10-10 at 17:55:24 UTC
Finalization Time: 2022-10-10 at 18:20:16 UTC
"""

from aioextensions import (
    collect,
    run,
)
from authz import (
    FLUID_IDENTIFIER,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.vulnerabilities.constants import (
    ASSIGNED_INDEX_METADATA,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
from dynamodb import (
    keys,
    operations,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import simplejson as json
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _process_vulnerability(
    vuln: Vulnerability,
    group_name: str,
) -> None:
    if (
        not vuln.treatment
        or not vuln.treatment.assigned
        or not vuln.treatment.assigned.endswith(FLUID_IDENTIFIER)
    ):
        return

    treatment_mod: VulnerabilityTreatment = vuln.treatment._replace(
        assigned=None
    )
    treatment_item = json.loads(json.dumps(treatment_mod))

    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": vuln.finding_id, "id": vuln.id},
    )
    gsi_3_index = TABLE.indexes["gsi_3"]
    gsi_3_key = keys.build_key(
        facet=ASSIGNED_INDEX_METADATA,
        values={
            "email": "",
            "vuln_id": vuln.id,
        },
    )
    metadata_item = {
        "treatment": treatment_item,
        gsi_3_index.primary_key.partition_key: gsi_3_key.partition_key,
        gsi_3_index.primary_key.sort_key: gsi_3_key.sort_key,
    }
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=metadata_item,
        key=metadata_key,
        table=TABLE,
    )

    historic_treatment_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_treatment"],
        values={
            "id": vuln.id,
            "iso8601utc": vuln.treatment.modified_date,  # type: ignore
        },
    )
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists()
        & Attr(key_structure.sort_key).eq(historic_treatment_key.sort_key),
        item={"assigned": None},
        key=historic_treatment_key,
        table=TABLE,
    )

    LOGGER_CONSOLE.info(
        "Vulnerability updated",
        extra={
            "extra": {
                "group_name": group_name,
                "finding_id": vuln.finding_id,
                "vuln_id": vuln.id,
            }
        },
    )


async def _process_finding(
    loaders: Dataloaders,
    finding_id: str,
    group_name: str,
) -> None:
    await collect(
        tuple(
            _process_vulnerability(vuln=vuln, group_name=group_name)
            for vuln in await loaders.finding_vulnerabilities.load(finding_id)
        ),
        workers=4,
    )


async def _process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    findings = await loaders.group_drafts_and_findings.load(group_name)
    await collect(
        tuple(
            _process_finding(
                loaders=loaders, finding_id=finding_id, group_name=group_name
            )
            for finding_id in [finding.id for finding in findings]
        ),
        workers=4,
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
    active_group_names = sorted(
        [
            group.name
            for group in active_groups
            if group.organization_id
            not in {
                "ORG#e8d37426-c999-4fd2-a0f3-b408f7a2175e",  # mura
                "ORG#0d6d8f9d-3814-48f8-ba2c-f4fb9f8d4ffa",  # imamura
            }
        ]
    )
    LOGGER_CONSOLE.info(
        "Active groups",
        extra={"extra": {"groups_len": len(active_group_names)}},
    )
    await collect(
        tuple(
            _process_group(
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
