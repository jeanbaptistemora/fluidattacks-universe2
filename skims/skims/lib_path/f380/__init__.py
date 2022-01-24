from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_YAML,
    NAMES_DOCKERFILE,
    SHIELD,
)
from lib_path.f380.docker import (
    unpinned_docker_image,
)
from model.core_model import (
    Vulnerabilities,
)
import re
from typing import (
    Awaitable,
    Callable,
    List,
)
from utils.function import (
    TIMEOUT_1MIN,
)


@SHIELD
@TIMEOUT_1MIN
async def run_unpinned_docker_image(
    content: str, path: str
) -> Vulnerabilities:
    return await in_process(
        unpinned_docker_image,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []

    if (file_name in NAMES_DOCKERFILE and file_extension == "") or (
        re.search("docker", file_name, re.IGNORECASE)
        and file_extension in EXTENSIONS_YAML
    ):
        coroutines.append(run_unpinned_docker_image(content_generator(), path))

    return coroutines
