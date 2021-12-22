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
from custom_exceptions import (
    VulnNotFound,
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
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities import (
    utils as db_model_utils,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityHistoric,
)
from dynamodb import (
    keys,
    operations,
    operations_legacy,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
from newutils import (
    vulnerabilities as vulns_utils,
)
from newutils.vulnerabilities import (
    adjust_historic_dates,
)
import simplejson as json  # type: ignore
import time
from typing import (
    List,
    Optional,
)

PROD: bool = False


async def _add_historic(
    *,
    historic: VulnerabilityHistoric,
    vulnerability_id: str,
) -> None:
    key_structure = TABLE.primary_key
    latest_entry = historic[-1]
    entry_type = db_model_utils.historic_entry_type_to_str(latest_entry)

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


async def _get_vulnerability_vms(vuln_id: str) -> Optional[Vulnerability]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"id": vuln_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_metadata"],),
        table=TABLE,
    )
    if not response.items:
        return None
    return db_model_utils.format_vulnerability(response.items[0])


async def _get_vulnerability_old(vuln_id: str) -> Vulnerability:
    hash_key = "UUID"
    query_attrs = {
        "IndexName": "gsi_uuid",
        "KeyConditionExpression": Key(hash_key).eq(vuln_id),
    }
    items = await operations_legacy.query("FI_vulnerabilities", query_attrs)
    if not items:
        raise VulnNotFound()
    return vulns_utils.format_vulnerability(items[0])


async def _add_metadata(vulnerability: Vulnerability) -> None:
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


def _log(
    group_name: str, finding_id: str, vuln_id: str, status: str, result: bool
) -> str:
    msg = f"{group_name},{finding_id},{vuln_id},{status},{result}"
    print(msg)
    return msg


async def _process_vulnerability(
    *,
    loaders: Dataloaders,
    group_name: str,
    finding_id: str,
    vuln_id: str,
) -> str:
    current_vuln = await _get_vulnerability_old(vuln_id)
    if current_vuln.state.status == VulnerabilityStateStatus.DELETED:
        return _log(group_name, finding_id, vuln_id, "DELETED", False)

    state_loader = loaders.vulnerability_historic_state
    treatment_loader = loaders.vulnerability_historic_treatment
    verification_loader = loaders.vulnerability_historic_verification
    zero_risk_loader = loaders.vulnerability_historic_zero_risk
    state_loader.clear(vuln_id)
    treatment_loader.clear(vuln_id)
    verification_loader.clear(vuln_id)
    zero_risk_loader.clear(vuln_id)
    historic_state = adjust_historic_dates(await state_loader.load(vuln_id))
    historic_treatment = adjust_historic_dates(
        await treatment_loader.load(vuln_id)
    )
    historic_verification = adjust_historic_dates(
        await verification_loader.load(vuln_id)
    )
    historic_zero_risk = adjust_historic_dates(
        await zero_risk_loader.load(vuln_id)
    )
    current_vuln = current_vuln._replace(
        state=historic_state[-1],
        treatment=historic_treatment[-1] if historic_treatment else None,
        verification=historic_verification[-1]
        if historic_verification
        else None,
        zero_risk=historic_zero_risk[-1] if historic_zero_risk else None,
    )

    vuln_in_vms = await _get_vulnerability_vms(vuln_id)
    if current_vuln == vuln_in_vms:
        return _log(group_name, finding_id, vuln_id, "ALREADY_MIGRATED", True)

    if not PROD:
        return _log(group_name, finding_id, vuln_id, "NOT_PROD", False)

    await _add_metadata(vulnerability=current_vuln)
    await _add_historic(
        historic=historic_state,
        vulnerability_id=vuln_id,
    )
    if historic_treatment:
        await _add_historic(
            historic=historic_treatment,
            vulnerability_id=vuln_id,
        )
    if historic_verification:
        await _add_historic(
            historic=historic_verification,
            vulnerability_id=vuln_id,
        )
    if historic_zero_risk:
        await _add_historic(
            historic=historic_zero_risk,
            vulnerability_id=vuln_id,
        )

    return _log(group_name, finding_id, vuln_id, "MIGRATED", True)


async def _process_finding(
    *,
    loaders: Dataloaders,
    finding: Finding,
) -> List[str]:
    vulns = await loaders.finding_vulns_typed.load(finding.id)
    vulns_uuids = [vuln.id for vuln in vulns]
    return list(
        await collect(
            tuple(
                _process_vulnerability(
                    loaders=loaders,
                    group_name=finding.group_name,
                    finding_id=finding.id,
                    vuln_id=vuln_id,
                )
                for vuln_id in vulns_uuids
            ),
            workers=64,
        )
    )


async def _process_group(
    *,
    loaders: Dataloaders,
    group_name: str,
) -> List[str]:
    findings_loader = loaders.group_drafts_and_findings
    findings = await findings_loader.load(group_name)
    print(f" - group {group_name} : {len(findings)} findings")
    return list(
        chain.from_iterable(
            await collect(
                tuple(
                    _process_finding(
                        loaders=loaders,
                        finding=finding,
                    )
                    for finding in findings
                ),
                workers=128,
            )
        )
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await groups_domain.get_active_groups())
    print(f"groups({len(group_names)}): {group_names}")

    for group_name in group_names:
        start = time.time()
        results = await _process_group(loaders=loaders, group_name=group_name)
        success = all(item.split(",")[-1] == "True" for item in results)
        print(
            f" - group {group_name} FINISHED in "
            f"{timedelta(seconds=time.time() - start)} - "
            f"results({len(results)}), success: {success}"
        )

        csv_file = "0165_results.csv"
        with open(csv_file, "a", encoding="utf8") as f:
            for item in results:
                f.write(f"{item}\n")

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
