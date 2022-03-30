from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
import re
from typing import (
    Iterator,
    Optional,
    Tuple,
)

COMMANDS_REGEX = [
    re.compile(r"^RUN.*useradd"),
    re.compile(r"^RUN.*adduser"),
    re.compile(r"^RUN.*addgroup"),
    re.compile(r"^RUN.*usergroup"),
    re.compile(r"^RUN.*usermod"),
    re.compile(r"^USER"),
]


def get_container_image(content: str) -> Optional[Tuple[int, int]]:
    for line_number, line in enumerate(content.splitlines(), start=1):
        if re.match(r"FROM\s+\S+", line):
            return line_number, 0
    return None


def container_whitout_user(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        has_user = False
        for _, line in enumerate(content.splitlines(), start=1):
            if any(regex.match(line) for regex in COMMANDS_REGEX):
                has_user = True
        if (lines := get_container_image(content)) and not has_user:
            yield lines

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f266.container_whitout_user",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.CONTAINER_WHITOUR_USER,
    )
