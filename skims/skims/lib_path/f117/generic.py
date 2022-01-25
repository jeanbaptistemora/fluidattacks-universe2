from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.function import (
    TIMEOUT_1MIN,
)


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def unverifiable_files(path: str, raw_content: bytes) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=raw_content.decode(encoding="utf-8", errors="replace"),
        cwe={"377"},
        description_key="src.lib_path.f117.unverifiable_files.description",
        finding=FindingEnum.F117,
        iterator=iter([(1, 0)]),
        path=path,
    )
