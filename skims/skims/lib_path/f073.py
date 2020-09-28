# Standard library
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Iterator,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)

# Local libraries
from parse_grammar import (
    parse,
)
from lib_path.common import (
    EXTENSIONS_JAVA,
    SHIELD,
    blocking_get_vulnerabilities_from_iterator,
)
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.graph import (
    yield_nodes,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)


def _java_switch_without_default(
    content: str,
    model: Dict[str, Any],
    path: str,
) -> Tuple[Vulnerability, ...]:

    def iterator() -> Iterator[Tuple[int, int]]:
        for switch in yield_nodes(
            value=model,
            key_predicates=(
                'SwitchStatement'.__eq__,
            ),
            pre_extraction=(),
            post_extraction=(),
        ):
            for labels in yield_nodes(
                value=switch,
                value_extraction='.'.join((
                    '[4]',
                    'SwitchBlock[1:-1]',
                    'SwitchBlockStatementGroup[]',
                    'SwitchLabels[0]',
                    'SwitchLabel[0]',
                    'text',
                )),
                pre_extraction=(),
                post_extraction=(),
            ):
                if labels and 'default' not in labels:
                    yield switch[0]['l'], switch[0]['c']

    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        description='src.lib_path.f073.switch_without_default',
        finding=FindingEnum.F073,
        iterator=iterator(),
        path=path,
    )


@cache_decorator()
@SHIELD
async def java_switch_without_default(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_switch_without_default,
        content=content,
        model=await parse(
            'Java9',
            content=content.encode(),
            path=path,
        ),
        path=path,
    )


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_switch_without_default(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
