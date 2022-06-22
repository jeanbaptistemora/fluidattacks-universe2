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
import os


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
        technique=method.value.technique,
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


def get_path_from_root(path: str) -> str:
    """
    When splitting monorepos in multiple subrepos,
    the file path obtained is relative to the subrepo
    while Skims expects it to be relative to the root of the repo
    """
    abs_path = os.path.abspath(path)

    # In most cases, the namespace is the name of the repostiory
    # and it is part of the absolute path of the file.
    # However, there may be cases
    # where the namespace is set to a completely differente value,
    # and the code breaks if this condition is assumed to always be true.
    # See product/skims/test/data/config/*.yaml for some examples
    if f"/{CTX.config.namespace}/" in abs_path:
        return abs_path.split(f"{CTX.config.namespace}/", maxsplit=1)[1]
    return path
