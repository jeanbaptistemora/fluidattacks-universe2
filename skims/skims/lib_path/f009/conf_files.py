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
    MethodsEnum,
    Vulnerabilities,
)
from pyparsing import (
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
        description_key="src.lib_path.f009.jwt_token.description",
        grammar=grammar,
        path=path,
        method=MethodsEnum.JWT_TOKEN,
    )


def web_config_db_connection(content: str, path: str) -> Vulnerabilities:
    grammar = Regex(
        r'connectionString=".*password=[^{]+.*"', flags=re.IGNORECASE
    )
    return get_vulnerabilities_blocking(
        content=content,
        description_key=(
            "src.lib_path.f009.web_config_db_connection.description"
        ),
        grammar=grammar,
        path=path,
        wrap=True,
        method=MethodsEnum.WEB_DB_CONN,
    )


def web_config_user_pass(content: str, path: str) -> Vulnerabilities:
    return get_vulnerabilities_blocking(
        content=content,
        description_key="src.lib_path.f009.web_config_user_pass.description",
        grammar=Regex(r'(username|password)=".+?"', flags=re.IGNORECASE),
        path=path,
        method=MethodsEnum.WEB_USER_PASS,
    )
