from ctx import (
    CTX,
)
from model.core_model import (
    MethodsEnum,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)


def build_metadata(
    method: MethodsEnum,
    description: str,
    snippet: str,
) -> SkimsVulnerabilityMetadata:
    return SkimsVulnerabilityMetadata(
        cwe=(method.value.get_cwe(),),
        description=description,
        snippet=snippet,
        source_method=method.value.get_name(),
        developer=method.value.developer,
    )


def build_inputs_vuln(
    method: MethodsEnum,
    stream: str,
    what: str,
    where: str,
    metadata: SkimsVulnerabilityMetadata,
) -> Vulnerability:
    return Vulnerability(
        finding=method.value.finding,
        kind=VulnerabilityKindEnum.INPUTS,
        namespace=CTX.config.namespace,
        state=VulnerabilityStateEnum.OPEN,
        stream=stream,
        what=what,
        where=where,
        skims_metadata=metadata,
    )


def build_lines_vuln(
    method: MethodsEnum,
    what: str,
    where: str,
    metadata: SkimsVulnerabilityMetadata,
) -> Vulnerability:
    return Vulnerability(
        finding=method.value.finding,
        kind=VulnerabilityKindEnum.LINES,
        namespace=CTX.config.namespace,
        state=VulnerabilityStateEnum.OPEN,
        what=what,
        where=where,
        skims_metadata=metadata,
    )


def build_ports_vuln(
    method: MethodsEnum,
    what: str,
    where: str,
    metadata: SkimsVulnerabilityMetadata,
) -> None:
    # pylint: disable=unused-argument
    # skims does not produce ports vulnerabilities at the moment
    pass
