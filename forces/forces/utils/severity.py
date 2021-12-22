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
        for finding in findings:
            for vuln in finding["vulnerabilities"]:
                if (
                    vuln["state"] == "open"
                    and finding["severity"] >= config.breaking_severity
                ):
                    await log(
                        "warning",
                        (
                            "Found at least one open vulnerability with a "
                            f"severity of {finding['severity']} >= "
                            f"{config.breaking_severity}"
                        ),
                    )
                    return 1
        # Forces didn't find open vulns or none of the open vulns' severity
        # warrant a failing exit code
        await log(
            "info",
            (
                "[green]No open vulnerabilities with a severity above this"
                " threshold found[/]"
            ),
        )
    # Forces wasn't set to strict mode or there aren't any findings yet
    return 0
