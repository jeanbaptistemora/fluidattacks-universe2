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
import re


def web_config_user_pass(content: str, path: str) -> Vulnerabilities:
    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description_key="src.lib_path.f009.web_config_user_pass.description",
        finding=FindingEnum.F009,
        grammar=Regex(r'(username|password)=".+?"', flags=re.IGNORECASE),
        path=path,
    )
