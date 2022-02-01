from lib_path.common import (
    get_vulnerabilities_blocking,
)
from model.core_model import (
    MethodsEnum,
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
            if re.fullmatch(
                r"FROM\s+[\w\/]+(\s+AS\s+\S+)?", token
            ) or re.fullmatch(
                r"FROM\s+[\w\/]+:[\w\-\.]+(\s+AS\s+\S+)?", token
            ):
                return True
        return False

    grammar = Regex(r"FROM\s+\S+")
    grammar.addCondition(check_regex)

    return get_vulnerabilities_blocking(
        content=content,
        description_key="criteria.vulns.380.description",
        grammar=grammar,
        path=path,
        method=MethodsEnum.UNPINNED_DOCKER_IMAGE,
    )
