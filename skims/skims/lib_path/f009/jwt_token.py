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
    Regex,
)


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
