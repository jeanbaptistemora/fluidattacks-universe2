from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
import re
from typing import (
    Iterator,
    Pattern,
    Set,
    Tuple,
)

# Constants
WS = r"\s*"
WSM = r"\s+"
DOCKERFILE_ENV: Pattern[str] = re.compile(
    fr"^{WS}ENV{WS}(?P<key>[\w\.]+)(?:{WS}={WS}|{WSM})(?P<value>.+?){WS}$",
)


def _is_key_sensitive(key: str) -> bool:
    return any(
        key.lower().endswith(suffix)
        for suffix in [
            "key",
            "pass",
            "passwd",
            "user",
            "username",
        ]
    )


def dockerfile_env_secrets(content: str, path: str) -> Vulnerabilities:
    secret_smells: Set[str] = {
        "api_key",
        "jboss_pass",
        "license_key",
        "password",
        "secret",
    }

    def iterator() -> Iterator[Tuple[int, int]]:
        for line_no, line in enumerate(content.splitlines(), start=1):
            if match := DOCKERFILE_ENV.match(line):
                secret: str = match.group("key").lower()
                value: str = match.group("value").strip('"').strip("'")
                if (
                    value
                    and not value.startswith("#{")
                    and not value.endswith("}#")
                    and (
                        any(smell in secret for smell in secret_smells)
                        or _is_key_sensitive(secret)
                    )
                ):
                    column: int = match.start("value")
                    yield line_no, column

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"798"},
        description_key="src.lib_path.f009.dockerfile_env_secrets.description",
        finding=FindingEnum.F009,
        iterator=iterator(),
        path=path,
    )
