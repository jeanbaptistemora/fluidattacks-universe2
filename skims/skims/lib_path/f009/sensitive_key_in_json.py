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


def sensitive_key_in_json(content: str, path: str) -> Vulnerabilities:
    key_smell = {
        "api_key",
        "current_key",
    }

    def check_key(tokens: ParseResults) -> bool:
        for token in tokens:
            key, _ = token.split(":", maxsplit=1)
            if key.strip(' "') in key_smell:
                return True
        return False

    grammar = Regex(r"\s*\"\w+\"\s*:\s*\"[A-Za-z0-9]{5,}\"")
    grammar.addCondition(check_key)

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description_key="src.lib_path.f009.sensitive_key_in_json.description",
        finding=FindingEnum.F009,
        grammar=grammar,
        path=path,
    )
