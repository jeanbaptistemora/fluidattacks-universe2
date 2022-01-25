from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    SHIELD_BLOCKING,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from state.cache import (
    CACHE_ETERNALLY,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def non_upgradeable_deps(path: str, raw_content: bytes) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=raw_content.decode(encoding="utf-8", errors="replace"),
        cwe={"829"},
        description_key="src.lib_path.f079.non_upgradeable_deps.description",
        finding=FindingEnum.F079,
        iterator=iter([(1, 0)]),
        path=path,
    )
