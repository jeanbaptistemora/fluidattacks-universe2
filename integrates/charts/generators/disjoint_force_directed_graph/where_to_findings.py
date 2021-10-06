from aioextensions import (
    run,
)
from charts import (
    utils,
)
from context import (
    FI_API_STATUS,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
)
from findings import (
    domain as findings_domain,
)
from frozendict import (  # type: ignore
    frozendict,
)
from typing import (
    Tuple,
)


async def generate_one(group: str) -> dict:
    context = get_new_context()
    data: dict = {
        "nodes": set(),
        "links": set(),
    }
    if FI_API_STATUS == "migration":
        group_findings_new_loader = context.group_findings_new
        group_findings_new: Tuple[
            Finding, ...
        ] = await group_findings_new_loader.load(group)
        group_findings_data = [
            (
                finding.id,
                finding.title,
                findings_domain.get_severity_score_new(finding.severity),
            )
            for finding in group_findings_new
        ]
    else:
        group_findings_loader = context.group_findings
        group_findings = await group_findings_loader.load(group)
        group_findings_data = [
            (
                finding["finding_id"],
                finding["title"],
                Decimal(finding.get("cvss_temporal", 0.0)).quantize(
                    Decimal("0.1")
                ),
            )
            for finding in group_findings
        ]
    for finding_id, finding_title, finding_cvss in group_findings_data:
        finding_vulns = await context.finding_vulns_nzr.load(finding_id)
        for vulnerability in finding_vulns:
            source = utils.get_vulnerability_source(vulnerability)
            target = f"{finding_title} {source}"

            data["nodes"].add(
                frozendict(
                    {
                        "group": "source",
                        "id": source,
                    }
                )
            )
            data["nodes"].add(
                frozendict(
                    {
                        "group": "target",
                        "id": target,
                        "score": float(finding_cvss),
                        "isOpen": vulnerability["current_state"] == "open",
                        "display": f"[{finding_cvss}] {finding_title}",
                    }
                )
            )
            data["links"].add(
                frozendict(
                    {
                        "source": source,
                        "target": target,
                    }
                )
            )

    return data


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity="group",
            subject=group,
        )


if __name__ == "__main__":
    run(generate_all())
