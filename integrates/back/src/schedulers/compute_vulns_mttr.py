from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    timedelta,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from findings.domain.core import (
    is_deleted,
)
from groups import (
    dal as groups_dal,
)
from newutils.datetime import (
    get_datetime_from_iso_str,
)
from typing import (
    cast,
    Dict,
    Tuple,
)


def compute_ttr(report_date: str, closing_date: str) -> timedelta:
    """Returns a vuln's time to remediate"""
    return get_datetime_from_iso_str(closing_date) - get_datetime_from_iso_str(
        report_date
    )


def mttr_to_hours(mttr: timedelta) -> float:
    """Returns the minimum time to remediate in hours from a timedelta"""
    return round(mttr.total_seconds() / 3600, 3)


async def compute_global_mttrs() -> Dict[int, float]:
    """Computes the mean time to remediate (MTTR) attr for every finding type.
    This is done by averaging the fastest closing cycles found for each of
    them"""
    global_mttr_helper: Dict[int, timedelta] = {}

    loaders: Dataloaders = get_new_context()
    group_names = sorted(
        [group["group_name"] for group in await groups_dal.get_alive_groups()]
    )

    for group_name in group_names:
        group_findings: Tuple[
            Finding, ...
        ] = await loaders.group_findings.load(group_name)
        valid_findings = [
            (finding.id, finding.title)
            for finding in group_findings
            if not is_deleted(finding)
        ]
        for finding_id, finding_title in valid_findings:
            closed_finding_vulns: Tuple[Vulnerability, ...] = tuple(
                cast(Vulnerability, vuln)
                for vuln in await loaders.finding_vulns_nzr_typed.load(
                    finding_id
                )
                if vuln.state.status == VulnerabilityStateStatus.CLOSED
            )

            if finding_title not in global_mttr_helper:
                global_mttr_helper[finding_title] = timedelta()

            # The minimum timedelta will be the mttr for each finding type
            for vuln in closed_finding_vulns:
                old_mttr = global_mttr_helper[finding_title]
                current_ttr = compute_ttr(
                    vuln.unreliable_indicators.unreliable_report_date,
                    vuln.state.modified_date,
                )
                if old_mttr == timedelta():
                    global_mttr_helper[finding_title] = current_ttr
                else:
                    global_mttr_helper[finding_title] = min(
                        old_mttr, current_ttr
                    )
    # Map minimum timedelta to remediate (mttr) to floats (hours)
    global_mttr: Dict[int, float] = {
        finding_title: mttr_to_hours(mttr)
        for finding_title, mttr in sorted(global_mttr_helper.items())
        if mttr > timedelta()
    }
    # Update mttr table
    return global_mttr
