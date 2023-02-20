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
    VulnerabilityState,
)
from forces.utils.logs import (
    log,
)


def set_breaking_severity(
    arm_severity_policy: float | None, cli_severity_policy: float | None
) -> Decimal:
    """Gets the breaking severity policy for the strict mode, defaults to 0.0

    Args:
        `arm_severity_policy (float | None)`: The value set in ARM's policies
        `cli_severity_policy (float | None)`: The value set in the CLI

    Returns:
        `Decimal`: `min(arm, cli)` if both exist, ARM value otherwise,
        local otherwise, 0.0 otherwise
    """
    if arm_severity_policy is not None and cli_severity_policy is not None:
        return Decimal(str(min(arm_severity_policy, cli_severity_policy)))
    if arm_severity_policy is not None:
        return Decimal(str(arm_severity_policy))
    if cli_severity_policy is not None:
        return Decimal(str(cli_severity_policy))
    return Decimal("0.0")


def get_policy_compliance(
    config: ForcesConfig,
    report_date: datetime,
    severity: Decimal,
    state: VulnerabilityState,
) -> bool:
    """
    Returns `True` if the vulnerability complies with the Agent strict mode
    policies (severity threshold & grace period), `False` otherwise
    """
    current_date: datetime = datetime.now(tz=timezone.utc)
    time_diff: timedelta = current_date - report_date
    return not (
        state == VulnerabilityState.VULNERABLE
        and severity >= config.breaking_severity
        and abs(time_diff.days) >= config.grace_period
    )


async def set_forces_exit_code(
    config: ForcesConfig, findings: tuple[Finding, ...]
) -> int:
    if config.strict:
        await log(
            "info",
            (
                "Checking for [red]vulnerable[/] spots with a "
                "[bright_yellow]severity[/] score of "
                f"{config.breaking_severity} and above"
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
                if not vuln.compliance:
                    current_date: datetime = datetime.now(tz=timezone.utc)
                    time_diff: timedelta = current_date - vuln.report_date
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
                "[green]No vulnerable spots with a severity above this"
                " threshold and outside the set grace period were found[/]"
            ),
        )
    # Forces wasn't set to strict mode or there aren't any findings yet
    return 0
