from ctx import (
    STATE_FOLDER_DEBUG,
)
from io import (
    BytesIO,
)
import os
from utils.logs import (
    log_blocking,
)


def to_in_memory_file(string: str) -> BytesIO:
    return BytesIO(string.encode())


def get_debug_path(path: str) -> str:
    output = os.path.join(
        STATE_FOLDER_DEBUG,
        os.path.relpath(path).replace("/", "__").replace(".", "_"),
    )
    log_blocking("info", "An output will be generated at %s*", output)
    return output


def build_attr_paths(*attrs: str) -> set[str]:
    return set(".".join(attrs[index:]) for index, _ in enumerate(attrs))


def split_on_first_dot(string: str) -> tuple[str, str]:
    portions = string.split(".", maxsplit=1)
    if len(portions) == 2:
        return portions[0], portions[1]
    return portions[0], ""


def split_on_last_dot(string: str) -> tuple[str, str]:
    portions = string.rsplit(".", maxsplit=1)
    if len(portions) == 2:
        return portions[0], portions[1]
    return portions[0], ""


def complete_attrs_on_set(data: set[str]) -> set[str]:
    return {
        attr for path in data for attr in build_attr_paths(*path.split("."))
    }
