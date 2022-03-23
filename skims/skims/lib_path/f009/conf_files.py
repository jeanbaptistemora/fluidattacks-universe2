from jose.exceptions import (
    JOSEError,
)
from jose.jwt import (
    decode as jwt_decode,
)
from lib_path.common import (
    get_vulnerabilities_blocking,
    get_vulnerabilities_from_iterator_blocking,
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
from typing import (
    Any,
    Iterator,
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
        description_key="src.lib_path.f009.jwt_token.description",
        grammar=grammar,
        path=path,
        method=MethodsEnum.JWT_TOKEN,
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
        description_key="src.lib_path.f009.sensitive_key_in_json.description",
        grammar=grammar,
        path=path,
        method=MethodsEnum.SENSITIVE_KEY_JSON,
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


def _sensitive_info_in_dotnet_json(
    template: Any,
) -> Iterator[Any]:
    regex_email = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    services = template.inner.get("OutlookServices")
    if (
        services
        and services.inner.get("Email")
        and services.inner.get("Password")
        and isinstance(services.inner.get("Email").data, str)
        and re.fullmatch(
            regex_email,
            services.inner.get("Email").data,
        )
    ):
        yield services.start_line, services.start_column


def sensitive_info_in_dotnet_json(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f009.sensitive_key_in_json.description",
        iterator=_sensitive_info_in_dotnet_json(
            template=template,
        ),
        path=path,
        method=MethodsEnum.SENSITIVE_INFO_DOTNET_JSON,
    )


def _sensitive_info_in_json(
    template: Any,
) -> Iterator[Any]:
    regex_password = re.compile(r"Password=.*")
    connection_str = template.inner.get("ConnectionStrings")
    if connection_str and connection_str.inner.get("Claims"):
        data_str = connection_str.inner.get("Claims").data
        for element in data_str.split(";"):
            if re.match(regex_password, element):
                yield connection_str.start_line, connection_str.start_column


def sensitive_info_in_json(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f009.sensitive_key_in_json.description",
        iterator=_sensitive_info_in_json(
            template=template,
        ),
        path=path,
        method=MethodsEnum.SENSITIVE_INFO_JSON,
    )
