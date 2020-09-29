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
from parse_antlr import (
    parse as parse_antlr,
)
from parse_babel import (
    parse as parse_babel,
)
from lib_path.common import (
    EXTENSIONS_JAVA,
    EXTENSIONS_JAVASCRIPT,
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
    yield_dicts,
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
        model=await parse_antlr(
            'Java9',
            content=content.encode(),
            path=path,
        ),
        path=path,
    )


def _javascript_switch_without_default(
    content: str,
    model: Dict[str, Any],
    path: str,
) -> Tuple[Vulnerability, ...]:

    def iterator() -> Iterator[Tuple[int, int]]:
        for node in yield_dicts(model):
            # interface SwitchStatement <: Statement {
            #     #type: "SwitchStatement";
            #     discriminant: Expression;
            #     cases: [ SwitchCase ];
            # }
            if node.get('type') == 'SwitchStatement':
                # interface SwitchCase <: Node {
                #     #type: "SwitchCase";
                #     test: Expression | null;
                #     consequent: [ Statement ];
                # }
                #
                # A case (if test is an Expression) or default
                # (if test === null) clause in the body of a switch statement.
                defaults_count: int = sum(
                    1 for case in node.get('cases', []) if case['test'] is None
                )
                if defaults_count == 0:
                    yield (
                        node['loc']['start']['line'],
                        node['loc']['start']['column'],
                    )

    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        description='src.lib_path.f073.switch_without_default',
        finding=FindingEnum.F073,
        iterator=iterator(),
        path=path,
    )


@SHIELD
async def javascript_switch_without_default(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _javascript_switch_without_default,
        content=content,
        model=await parse_babel(
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
    elif file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(javascript_switch_without_default(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
