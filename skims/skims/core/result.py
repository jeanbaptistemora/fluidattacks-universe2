from contextlib import (
    suppress,
)
from ctx import (
    CRITERIA_REQUIREMENTS,
    CRITERIA_VULNERABILITIES,
)
import hashlib
from model import (
    core_model,
)
import re
import sarif_om
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
    Dict,
    Optional,
    Union,
)
from utils.repositories import (
    get_repo_branch,
    get_repo_head_hash,
    get_repo_remote,
)
import yaml


def simplify_sarif(obj: Any) -> Any:
    simplified_obj: Any
    if hasattr(obj, "__attrs_attrs__"):
        simplified_obj = {
            attribute.metadata["schema_property_name"]: simplify_sarif(
                obj.__dict__[attribute.name]
            )
            for attribute in obj.__attrs_attrs__
            if obj.__dict__[attribute.name] != attribute.default
        }
    elif isinstance(obj, dict):
        simplified_obj = simplified_obj = {
            key: simplify_sarif(value) for key, value in obj.items()
        }
    elif isinstance(obj, (list, tuple, set)):
        simplified_obj = [simplify_sarif(item) for item in obj]
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
    auto_approve = False
    with suppress(KeyError):
        auto_approve = core_model.FindingEnum[f"F{vuln_id}"].value.auto_approve

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
        properties={"auto_approve": auto_approve},
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


def _get_sca_info(what: str) -> Optional[Dict[str, Any]]:
    try:
        str_info = what.split(" ", maxsplit=1)[1]
    except IndexError:
        return None
    if match := re.match(
        r"\((?P<name>(\S+)) v(?P<version>(.+))\) \[(?P<cve>(.+))\]", str_info
    ):
        match_dict = match.groupdict()
        return dict(
            dependency_name=match_dict["name"],
            dependency_version=match_dict["version"],
            cve=match_dict["cve"].split(", "),
        )
    return None


def _get_missing_dependency(what: str) -> Optional[Dict[str, Any]]:
    try:
        str_info = what.split(" ", maxsplit=1)[1]
    except IndexError:
        return None
    if match := re.match(r"\(missing dependency: (?P<name>(.+))\)$", str_info):
        match_dict = match.groupdict()
        return dict(
            dependency_name=match_dict["name"],
        )

    return None


def _format_what(what: str) -> str:
    return re.sub(r"\s(\(.*?\))((\s)(\[.*?\]))?", "", what)  # NOSONAR


def _format_were(were: str) -> Union[int, str]:
    try:
        return int(were)
    except ValueError:
        return were


def _get_vuln_properties(
    vulnerability: core_model.Vulnerability, rule_id: str
) -> Dict[str, Any]:
    properties: Dict[str, Any] = {}
    if (
        vulnerability.skims_metadata.technique == core_model.TechniqueEnum.SCA
        and (sca_info := _get_sca_info(vulnerability.what))
    ):
        properties = sca_info
    elif (
        (
            vulnerability.skims_metadata.source_method
            == "python.pip_incomplete_dependencies_list"
        )
        and rule_id == "120"
        and (dependency_info := _get_missing_dependency(vulnerability.what))
    ):
        properties = dependency_info

    return properties


def _get_sarif(
    config: core_model.SkimsConfig,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> sarif_om.SarifLog:
    base = sarif_om.SarifLog(
        version="2.1.0",
        schema_uri=(
            "https://schemastore.azurewebsites.net/schemas/"
            "json/sarif-2.1.0-rtm.4.json"
        ),
        runs=[
            sarif_om.Run(
                tool=sarif_om.Tool(
                    driver=sarif_om.ToolComponent(
                        name="skims",
                        rules=[],
                    )
                ),
                results=[],
                version_control_provenance=[
                    sarif_om.VersionControlDetails(
                        repository_uri=get_repo_remote(config.working_dir),
                        revision_id=get_repo_head_hash(config.working_dir),
                        branch=get_repo_branch(config.working_dir),
                    )
                ],
                taxonomies=[
                    sarif_om.ToolComponent(
                        name="criteria",
                        version="1",
                        information_uri=(
                            "https://docs.fluidattacks.com/"
                            "criteria/requirements/"
                        ),
                        organization="Fluidattacks",
                        short_description=sarif_om.MultiformatMessageString(
                            text="The fluidattacks security requirements"
                        ),
                        taxa=[],
                        is_comprehensive=False,
                    )
                ],
                original_uri_base_ids={
                    "SRCROOT": sarif_om.ArtifactLocation(uri=config.namespace)
                },
            ),
        ],
    )

    for check in config.checks:
        base.runs[0].tool.driver.rules.append(
            _get_rule(check.name.replace("F", ""))
        )

    for store in stores.values():
        for vulnerability in store.iterate():
            # remove F from findings
            rule_id = vulnerability.finding.name.replace("F", "")
            properties = _get_vuln_properties(vulnerability, rule_id)

            result = sarif_om.Result(
                rule_id=rule_id,
                level="error",
                kind="open",
                message=sarif_om.MultiformatMessageString(
                    text=(
                        vulnerability.skims_metadata.description
                        if vulnerability.skims_metadata
                        else ""
                    ),
                    properties=properties,
                ),
                locations=[
                    sarif_om.Location(
                        physical_location=sarif_om.PhysicalLocation(
                            artifact_location=sarif_om.ArtifactLocation(
                                uri=_format_what(vulnerability.what)
                            ),
                            region=sarif_om.Region(
                                start_line=_format_were(vulnerability.where),
                                snippet=sarif_om.MultiformatMessageString(
                                    text=vulnerability.skims_metadata.snippet
                                    if vulnerability.skims_metadata
                                    else ""
                                ),
                            ),
                        )
                    ),
                ],
                taxa=[],
                properties={
                    "kind": vulnerability.kind.value,
                    "method_developer": (
                        vulnerability.skims_metadata.developer.value
                    ),
                    "source_method": (
                        vulnerability.skims_metadata.source_method
                    ),
                    "stream": vulnerability.stream,
                    "technique": (
                        vulnerability.skims_metadata.technique.value
                    ),
                    **(
                        vulnerability.skims_metadata.http_properties._asdict()
                        if vulnerability.skims_metadata.http_properties
                        is not None
                        else {}
                    ),
                },
            )
            result.guid = int.from_bytes(
                hashlib.sha256(
                    bytes(
                        (
                            result.locations[
                                0
                            ].physical_location.artifact_location.uri
                            + str(
                                result.locations[
                                    0
                                ].physical_location.region.start_line
                            )
                            + rule_id
                            + vulnerability.skims_metadata.source_method
                        ),
                        "utf-8",
                    )
                ).digest()[:8],
                "little",
            )

            # append rule if not is present
            if not _rule_is_present(base, rule_id):
                base.runs[0].tool.driver.rules.append(_get_rule(rule_id))

            # append requirement if not is present
            for taxa_id in CRITERIA_VULNS[rule_id]["requirements"]:
                if not _taxa_is_present(base, taxa_id):
                    base.runs[0].taxonomies[0].taxa.append(_get_taxa(taxa_id))
                result.taxa.append(
                    sarif_om.ReportingDescriptorReference(
                        id=taxa_id,
                        tool_component=sarif_om.ToolComponentReference(
                            name="criteria"
                        ),
                    )
                )
            base.runs[0].results.append(result)

    return base


def get_sarif(
    config: core_model.SkimsConfig,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> Dict[str, Any]:
    return simplify_sarif(_get_sarif(config, stores))
