# pylint: disable=invalid-name
"""
This migration aims to populate vulns from FI_vulnerabilities to
integrates_vms.

We'll keep deleted items out of the new model while we define the path
going forward for archived data.
Details at https://gitlab.com/fluidattacks/product/-/issues/5690

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    timedelta,
)
from db_model import (
    TABLE,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityHistoric,
)
from db_model.vulnerabilities.utils import (
    historic_entry_type_to_str,
)
from dynamodb import (
    keys,
    operations,
)
from groups import (
    domain as groups_domain,
)
from newutils.vulnerabilities import (
    adjust_historic_dates,
)
import simplejson as json  # type: ignore
import time

PROD: bool = False


def _log(vuln: Vulnerability, progress: float, result: bool) -> str:
    msg = f"{vuln.finding_id},{vuln.id},{progress:.4f},{result}"
    print(msg)
    return msg


async def _add_historic(
    *,
    historic: VulnerabilityHistoric,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    latest_entry = historic[-1]
    entry_type = historic_entry_type_to_str(latest_entry)

    historic_key = keys.build_key(
        facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
        values={"id": vulnerability_id},
    )
    current_response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
            & Key(key_structure.sort_key).begins_with(historic_key.sort_key)
        ),
        facets=(TABLE.facets[f"vulnerability_historic_{entry_type}"],),
        table=TABLE,
    )
    current_items = current_response.items
    current_keys = {
        keys.build_key(
            facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
            values={
                "id": vulnerability_id,
                "iso8601utc": item["sk"].split("#")[1],
            },
        )
        for item in current_items
    }

    new_keys = tuple(
        keys.build_key(
            facet=TABLE.facets[f"vulnerability_historic_{entry_type}"],
            values={
                "id": vulnerability_id,
                "iso8601utc": entry.modified_date,
            },
        )
        for entry in historic
    )
    new_items = tuple(
        {
            key_structure.partition_key: key.partition_key,
            key_structure.sort_key: key.sort_key,
            **json.loads(json.dumps(entry)),
        }
        for key, entry in zip(new_keys, historic)
    )
    await operations.batch_write_item(items=new_items, table=TABLE)
    await operations.batch_delete_item(
        keys=tuple(key for key in current_keys if key not in new_keys),
        table=TABLE,
    )


async def _add_metadata(*, vulnerability: Vulnerability) -> None:
    key_structure = TABLE.primary_key
    vulnerability_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "id": vulnerability.id,
        },
    )
    vulnerability_item = {
        key_structure.partition_key: vulnerability_key.partition_key,
        key_structure.sort_key: vulnerability_key.sort_key,
        **json.loads(json.dumps(vulnerability)),
    }
    await operations.batch_write_item(
        items=(vulnerability_item,),
        table=TABLE,
    )


async def _process_vulnerability(
    loaders: Dataloaders,
    vuln: Vulnerability,
    progress: float,
) -> str:
    if vuln.state.status == VulnerabilityStateStatus.DELETED:
        return _log(vuln, progress, False)

    state_loader = loaders.vulnerability_historic_state
    treatment_loader = loaders.vulnerability_historic_treatment
    verification_loader = loaders.vulnerability_historic_verification
    zero_risk_loader = loaders.vulnerability_historic_zero_risk
    historic_state = adjust_historic_dates(await state_loader.load(vuln.id))
    historic_treatment = adjust_historic_dates(
        await treatment_loader.load(vuln.id)
    )
    historic_verification = adjust_historic_dates(
        await verification_loader.load(vuln.id)
    )
    historic_zero_risk = adjust_historic_dates(
        await zero_risk_loader.load(vuln.id)
    )

    if not PROD:
        return _log(vuln, progress, False)

    await _add_metadata(
        vulnerability=vuln._replace(
            state=historic_state[-1],
            treatment=historic_treatment[-1] if historic_treatment else None,
            verification=historic_verification[-1]
            if historic_verification
            else None,
            zero_risk=historic_zero_risk[-1] if historic_zero_risk else None,
        )
    )
    await _add_historic(
        historic=historic_state,
        vulnerability_id=vuln.id,
    )
    if historic_treatment:
        await _add_historic(
            historic=historic_treatment,
            vulnerability_id=vuln.id,
        )
    if historic_verification:
        await _add_historic(
            historic=historic_verification,
            vulnerability_id=vuln.id,
        )
    if historic_zero_risk:
        await _add_historic(
            historic=historic_zero_risk,
            vulnerability_id=vuln.id,
        )

    return _log(vuln, progress, True)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await groups_domain.get_active_groups())
    print(f"groups({len(group_names)}): {group_names}")

    findings_loader = loaders.group_drafts_and_findings
    findings = await findings_loader.load_many_chained(group_names)
    finding_ids = [finding.id for finding in findings]
    print(f"findings({len(finding_ids)})")

    vulns_to_migrate = await loaders.finding_vulns_typed.load_many_chained(
        finding_ids
    )
    print(f"vulns to migrate({len(vulns_to_migrate)})")

    start = time.time()
    results = await collect(
        tuple(
            _process_vulnerability(
                loaders=loaders,
                vuln=vuln,
                progress=index / len(vulns_to_migrate),
            )
            for index, vuln in enumerate(vulns_to_migrate)
        ),
        workers=64,
    )
    print(f"processing time: {timedelta(seconds=time.time() - start)}")

    csv_file = "0165_results.csv"
    with open(csv_file, "w", encoding="utf8") as f:
        for item in results:
            f.write(f"{item}\n")

    print(f"results({len(results)})")
    success = all(item.split(",")[-1] == "True" for item in results)
    print(f"success: {success}")
    print("done!")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
