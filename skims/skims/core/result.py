from ctx import (
    CRITERIA_REQUIREMENTS,
    CRITERIA_VULNERABILITIES,
)
import sarif_om
from typing import (
    Any,
    Dict,
)
import yaml  # type: ignore


def _simplify(obj: Any) -> Any:
    simplified_obj: Any
    if hasattr(obj, "__attrs_attrs__"):
        simplified_obj = {
            attribute.metadata["schema_property_name"]: _simplify(
                obj.__dict__[attribute.name]
            )
            for attribute in obj.__attrs_attrs__
            if obj.__dict__[attribute.name] != attribute.default
        }
    elif isinstance(obj, (list, tuple, set)):
        simplified_obj = [_simplify(item) for item in obj]
    else:
        simplified_obj = obj
    return simplified_obj


def _get_criteria_vulns() -> Dict[str, Any]:
    with open(CRITERIA_VULNERABILITIES, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _get_criteria_requirements() -> Dict[str, Any]:
    with open(CRITERIA_REQUIREMENTS, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


CRITERIA_VULNS = _get_criteria_vulns()


CRITERIA_REQS = _get_criteria_requirements()


def _get_rule(vuln_id: str) -> sarif_om.ReportingDescriptor:
    content = CRITERIA_VULNS[vuln_id]
    return sarif_om.ReportingDescriptor(
        id=vuln_id,
        name=content["en"]["title"],
        full_description=sarif_om.MultiformatMessageString(
            text=content["en"]["description"]
        ),
        help_uri=(
            "https://docs.fluidattacks.com/criteria/"
            f"vulnerabilities/{vuln_id}#details"
        ),
        help=sarif_om.MultiformatMessageString(
            text=content["en"]["recommendation"]
        ),
        default_configuration=sarif_om.ReportingConfiguration(
            enabled=True, level="error"
        ),
    )


def _get_taxa(requirement_id: str) -> sarif_om.ReportingDescriptor:
    content = CRITERIA_REQS[requirement_id]
    return sarif_om.ReportingDescriptor(
        id=requirement_id,
        name=content["en"]["title"],
        short_description=sarif_om.MultiformatMessageString(
            text=content["en"]["summary"]
        ),
        full_description=sarif_om.MultiformatMessageString(
            text=content["en"]["description"]
        ),
        help_uri=(
            "https://docs.fluidattacks.com/criteria/"
            f"requirements/{requirement_id}"
        ),
    )


def _rule_is_present(base: sarif_om.SarifLog, rule_id: str) -> bool:
    for rule in base.runs[0].tool.driver.rules:
        if rule.id == rule_id:
            return True

    return False


def _taxa_is_present(base: sarif_om.SarifLog, taxa_id: str) -> bool:
    for rule in base.runs[0].taxonomies[0].taxa:
        if rule.id == taxa_id:
            return True

    return False


def _format_what(what: str) -> str:
    if " " in what:
        return what.split(" ")[0]
    return what
