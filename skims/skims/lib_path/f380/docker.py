from lib_path.common import (
    get_vulnerabilities_blocking,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from pyparsing import (
    ParseResults,
    Regex,
)
import re


def unpinned_docker_image(content: str, path: str) -> Vulnerabilities:
    def check_regex(tokens: ParseResults) -> bool:
        for token in tokens:
            if re.fullmatch(r"FROM\s+\w+:\S+", token) or re.fullmatch(
                r"FROM\s+\w+[^@]", token
            ):
                return True
        return False

    grammar = Regex(r"FROM\s+\S+")
    grammar.addCondition(check_regex)

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"749"},
        description_key="criteria.vulns.380.description",
        finding=FindingEnum.F380,
        grammar=grammar,
        path=path,
    )
