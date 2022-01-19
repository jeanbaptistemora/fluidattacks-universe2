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


def web_config_db_connection(content: str, path: str) -> Vulnerabilities:
    grammar = Regex(r'connectionString=".+?"', flags=re.IGNORECASE)
    grammar.addCondition(
        lambda tokens: any("password" in token.lower() for token in tokens)
    )

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description_key=(
            "src.lib_path.f009.web_config_db_connection.description"
        ),
        finding=FindingEnum.F009,
        grammar=grammar,
        path=path,
        wrap=True,
    )
