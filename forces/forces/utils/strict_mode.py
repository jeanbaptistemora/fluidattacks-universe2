from datetime import (
    datetime,
    timedelta,
)
from forces.utils.logs import (
    log,
)
from forces.utils.model import (
    ForcesConfig,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)


def choose_min_breaking_severity(
    global_brk_severity: Optional[float], local_brk_severity: Optional[float]
) -> float:
    global_brk_severity = (
        float(global_brk_severity) if global_brk_severity is not None else 0.0
    )
    return (
        float(local_brk_severity)
        if local_brk_severity is not None
        else global_brk_severity
    )


async def set_forces_exit_code(
    config: ForcesConfig, findings: List[Dict[str, Any]]
) -> int:
    if config.strict:
        await log(
            "info",
            (
                "Checking for [red]open[/] vulnerabilities with a "
                "[bright_yellow]severity[/] score over "
                f"{config.breaking_severity}"
            ),
        )
        await log(
            "info",
            (
                (
                    "Newly reported vulnerabilities' [bright_yellow]grace "
                    f"period[/] policy is set to {config.grace_period} day(s)"
                )
            ),
        )
        for finding in findings:
            for vuln in finding["vulnerabilities"]:
                severity: float = (
                    float(vuln["severity"])
                    if vuln["severity"] is not None
                    else float(finding["severity"])
                )
                current_date: datetime = datetime.utcnow()
                report_date: datetime = datetime.strptime(
                    vuln["report_date"], "%Y-%m-%d %H:%M:%S"
                )
                time_diff: timedelta = current_date - report_date
                if (
                    vuln["state"] == "open"
                    and severity >= config.breaking_severity
                    and time_diff.days >= config.grace_period
                ):
                    await log(
                        "warning",
                        (
                            "Found an open vulnerability with a severity of "
                            f"{severity} >= {config.breaking_severity} "
                            f"reported {time_diff.days} day(s) ago"
                        ),
                    )
                    return 1
        # Forces didn't find open vulns or none of the open vulns' severity
        # warrant a failing exit code
        await log(
            "info",
            (
                "[green]No open vulnerabilities with a severity above this"
                " threshold and outside the set grace period were found[/]"
            ),
        )
    # Forces wasn't set to strict mode or there aren't any findings yet
    return 0
