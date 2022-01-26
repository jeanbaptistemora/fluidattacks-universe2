from jose.exceptions import (
    JOSEError,
)
from jose.jwt import (
    decode as jwt_decode,
)
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


def _validate_jwt(token: str) -> bool:
    try:
        jwt_decode(
            token,
            key="",
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iat": False,
                "verify_exp": False,
                "verify_nbf": False,
                "verify_iss": False,
                "verify_sub": False,
                "verify_jti": False,
                "verify_at_hash": False,
                "leeway": 0,
            },
        )
        return True
    except JOSEError:
        return False


def jwt_token(content: str, path: str) -> Vulnerabilities:
    grammar = Regex(
        r"[A-Za-z0-9-_.+\/=]{20,}\."
        r"[A-Za-z0-9-_.+\/=]{20,}\."
        r"[A-Za-z0-9-_.+\/=]{20,}"
    )

    grammar.addCondition(
        lambda tokens: any(_validate_jwt(token) for token in tokens)
    )

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description_key="src.lib_path.f009.jwt_token.description",
        finding=FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


#  developer: asalgado@fluidattacks.com
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


#  developer: drestrepo@fluidattacks.com
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


#  developer: jrestrepo@fluidattacks.com
def web_config_user_pass(content: str, path: str) -> Vulnerabilities:
    return get_vulnerabilities_blocking(
        content=content,
        cwe={"798"},
        description_key="src.lib_path.f009.web_config_user_pass.description",
        finding=FindingEnum.F009,
        grammar=Regex(r'(username|password)=".+?"', flags=re.IGNORECASE),
        path=path,
    )
