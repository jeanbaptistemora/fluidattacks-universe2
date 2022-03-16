from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from re import (
    match,
)
from typing import (
    Iterator,
    Optional,
    Tuple,
)


def get_container_image(content: str) -> Optional[Tuple[int, int]]:
    for line_number, line in enumerate(content.splitlines(), start=1):
        if match(r"FROM\s+\S+", line):
            return line_number, 0
    return None


def container_whitout_user(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        root_group = True
        for _, line in enumerate(content.splitlines(), start=1):
            if match(r"^RUN.*useradd", line) or match(r"^USER", line):
                root_group = False
        if (lines := get_container_image(content)) and root_group:
            yield lines

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f266.container_whitout_user",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.CONTAINER_WHITOUR_USER,
    )
