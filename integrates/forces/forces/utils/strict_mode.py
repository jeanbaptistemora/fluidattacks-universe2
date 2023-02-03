from datetime import (
    datetime,
    timedelta,
    timezone,
)
from decimal import (
    Decimal,
)
from forces.model import (
    Finding,
    ForcesConfig,
    Vulnerability,
    VulnerabilityState,
)
from forces.utils.logs import (
    log,
)


def choose_min_breaking_severity(
    global_brk_severity: float | None, local_brk_severity: float | None
) -> Decimal:
    global_severity: Decimal = (
        Decimal(str(global_brk_severity))
        if global_brk_severity is not None
        else Decimal("0.0")
    )
    return (
        Decimal(str(local_brk_severity))
        if local_brk_severity is not None
        else global_severity
    )


def check_policy_compliance(config: ForcesConfig, vuln: Vulnerability) -> bool:
    """
    Returns `False` if the vulnerability does not comply with the Agent strict
    mode org policies (severity threshold and the grace period)
    """
    current_date: datetime = datetime.now(tz=timezone.utc)
    time_diff: timedelta = current_date - vuln.report_date
    return not (
        vuln.state == VulnerabilityState.VULNERABLE
        and vuln.severity >= config.breaking_severity
        and abs(time_diff.days) >= config.grace_period
    )


async def set_forces_exit_code(
    config: ForcesConfig, findings: tuple[Finding, ...]
) -> int:
    if config.strict:
        await log(
            "info",
            (
                "Checking for [red]vulnerable[/] areas with a "
                "[bright_yellow]severity[/] score over "
                f"{config.breaking_severity}"
            ),
        )
        await log(
            "info",
            (
                "Newly reported vulnerabilities' [bright_yellow]grace "
                f"period[/] policy is set to {config.grace_period} day(s)"
            ),
        )
        for finding in findings:
            for vuln in finding.vulnerabilities:
                current_date: datetime = datetime.now(tz=timezone.utc)
                time_diff: timedelta = current_date - vuln.report_date
                if not check_policy_compliance(config, vuln):
                    await log(
                        "warning",
                        (
                            f"In finding {finding.title}: Found a "
                            "vulnerability with a severity of "
                            f"{vuln.severity} reported {abs(time_diff.days)} "
                            "day(s) ago"
                        ),
                    )
                    return 1
        # Forces didn't find open vulns or none of the open vulns' severity
        # warrant a failing exit code
        await log(
            "info",
            (
                "[green]No vulnerable areas with a severity above this"
                " threshold and outside the set grace period were found[/]"
            ),
        )
    # Forces wasn't set to strict mode or there aren't any findings yet
    return 0
