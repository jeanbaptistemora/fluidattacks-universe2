from lib_path.common import (
    get_vulnerabilities_blocking,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from pyparsing import (
    Regex,
)


def aws_credentials(content: str, path: str) -> Vulnerabilities:
    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description_key="src.lib_path.f009.aws_credentials.description",
        finding=FindingEnum.F009,
        grammar=Regex(r"AKIA[A-Z0-9]{16}"),
        path=path,
    )
