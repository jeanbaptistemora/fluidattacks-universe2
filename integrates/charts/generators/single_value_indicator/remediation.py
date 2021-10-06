from aioextensions import (
    run,
)
from charts import (
    utils,
)
from charts.types import (
    RemediationReport,
)
from context import (
    FI_API_STATUS,
)
from custom_types import (
    Vulnerability as VulnerabilityType,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.findings.types import (
    Finding,
)
from itertools import (
    chain,
)
from typing import (
    List,
    Tuple,
)


def had_state_by_then(
    last_day: datetime, state: str, vuln: VulnerabilityType
) -> bool:
    historic_state = reversed(vuln["historic_state"])
    last_state: dict = next(
        filter(
            lambda item: datetime.strptime(item["date"], "%Y-%m-%d %H:%M:%S")
            <= last_day,
            historic_state,
        ),
        {},
    )

    return last_state.get("state") == state


def get_totals_by_week(
    vulns: List[VulnerabilityType], last_day: datetime
) -> Tuple[int, int]:
    open_vulnerabilities = len(
        tuple(
            filter(
                lambda vuln: had_state_by_then(
                    last_day=last_day,
                    state="open",
                    vuln=vuln,
                ),
                vulns,
            )
        )
    )
    closed_vulnerabilities = len(
        tuple(
            filter(
                lambda vuln: had_state_by_then(
                    last_day=last_day,
                    state="closed",
                    vuln=vuln,
                ),
                vulns,
            )
        )
    )

    return open_vulnerabilities, closed_vulnerabilities


async def generate_one(groups: Tuple[str, ...]) -> RemediationReport:
    context = get_new_context()
    finding_vulns_loader = context.finding_vulns_nzr
    if FI_API_STATUS == "migration":
        group_findings_new_loader = context.group_findings_new
        groups_findings_new: Tuple[
            Tuple[Finding, ...], ...
        ] = await group_findings_new_loader.load_many(groups)
        finding_ids = [
            finding.id
            for group_findings in groups_findings_new
            for finding in group_findings
        ]
    else:
        group_findings_loader = context.group_findings
        groups_findings_data = await group_findings_loader.load_many(groups)
        finding_ids = [
            finding["finding_id"]
            for group_findings in groups_findings_data
            for finding in group_findings
        ]

    current_rolling_week = datetime.now()
    previous_rolling_week = current_rolling_week - timedelta(days=7)

    vulns = list(
        chain.from_iterable(await finding_vulns_loader.load_many(finding_ids))
    )

    total_previous_open, total_previous_closed = get_totals_by_week(
        vulns,
        previous_rolling_week,
    )

    total_current_open, total_current_closed = get_totals_by_week(
        vulns,
        current_rolling_week,
    )

    return {
        "current": {
            "closed": total_current_closed,
            "open": total_current_open,
        },
        "previous": {
            "closed": total_previous_closed,
            "open": total_previous_open,
        },
        "totalGroups": len(groups),
    }


async def generate_all() -> None:
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=await generate_one(org_groups),
            entity="organization",
            subject=org_id,
        )


if __name__ == "__main__":
    run(generate_all())
