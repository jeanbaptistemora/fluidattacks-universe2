from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_YAML,
    get_vulnerabilities_blocking,
    NAMES_DOCKERFILE,
    SHIELD,
)
from model import (
    core_model,
)
from pyparsing import (
    ParseResults,
    Regex,
)
import re
from typing import (
    Awaitable,
    Callable,
    List,
)
from utils.ctx import (
    CTX,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from zone import (
    t,
)


def _unpinned_docker_image(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    def check_regex(tokens: ParseResults) -> bool:
        for token in tokens:
            if re.fullmatch(r"FROM\s+\w+:\S+", token) or re.fullmatch(
                r"FROM\s+\w+[^@]", token
            ):
                return True
        return False

    grammar = Regex(r"FROM\s+\S+")
    grammar.addCondition(check_regex)

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"749"},
        description=t(
            key="F380.description",
            path=f"{CTX.config.namespace}/{path}",
        ),
        finding=core_model.FindingEnum.F380,
        grammar=grammar,
        path=path,
    )


@SHIELD
@TIMEOUT_1MIN
async def unpinned_docker_image(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _unpinned_docker_image,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if (file_name in NAMES_DOCKERFILE and file_extension == "") or (
        re.search("docker", file_name, re.IGNORECASE)
        and file_extension in EXTENSIONS_YAML
    ):
        coroutines.append(
            unpinned_docker_image(
                content=await content_generator(),
                path=path,
            )
        )

    return coroutines
