from decimal import (
    Decimal,
)
from forces.model import (
    FindingState,
    VulnerabilityState,
    VulnerabilityType,
)


def style_severity(severity: Decimal) -> str:
    if Decimal("0.0") < severity < Decimal("4.0"):
        return f"[yellow3]{severity}[/]"
    if Decimal("4.0") <= severity < Decimal("7.0"):
        return f"[orange3]{severity}[/]"
    if Decimal("7.0") <= severity < Decimal("9.0"):
        return f"[bright_red]{severity}[/]"
    return f"[red]{severity}[/]"


def style_report(key: str, value: str) -> str:
    """Adds styles as rich console markup to the report values"""
    style_data = {
        "title": "[yellow]",
        "state": {
            FindingState.VULNERABLE: "[red]",
            FindingState.SAFE: "[green]",
            VulnerabilityState.VULNERABLE: "[red]",
            VulnerabilityState.SAFE: "[green]",
        },
        "exploit": {
            "Unproven": "[green]",
            "Proof of concept": "[yellow3]",
            "Functional": "[orange3]",
            "High": "[red]",
        },
        "type": {
            VulnerabilityType.DAST: "[thistle3]",
            VulnerabilityType.SAST: "[light_steel_blue1]",
        },
    }
    if key == "severity":
        return style_severity(Decimal(value))
    if key in style_data:
        value_style = style_data[key]
        if isinstance(value_style, dict):
            if value in value_style:
                return f"{value_style[value]}{value}[/]"
            return value
        return f"{value_style}{value}[/]"
    return str(value)


def style_summary(key: VulnerabilityState, value: int) -> str:
    """Adds styles as rich console markup to the summary values"""
    markup: str = ""
    if key == VulnerabilityState.ACCEPTED:
        return str(value)
    if key == VulnerabilityState.VULNERABLE:
        if value == 0:
            markup = "[green]"
        elif value < 10:
            markup = "[yellow3]"
        elif value < 20:
            markup = "[orange3]"
        else:
            markup = "[red]"
    elif key == VulnerabilityState.SAFE:
        markup = "[green]"
    return f"{markup}{str(value)}[/]"
