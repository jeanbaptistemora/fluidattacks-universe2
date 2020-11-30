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
import networkx as nx

# Local libraries
from parse_antlr.parse import (
    parse as parse_antlr,
)
from parse_babel import (
    parse as parse_babel,
)
from parse_java.parse import (
    parse_from_content as java_parse_from_content,
)
from lib_path.common import (
    EXTENSIONS_CSHARP,
    EXTENSIONS_JAVA,
    EXTENSIONS_JAVASCRIPT,
    SHIELD,
    blocking_get_vulnerabilities_from_iterator,
    blocking_get_vulnerabilities_from_n_attrs_iterator,
)
from state.cache import (
    CACHE_1SEC,
    CACHE_ETERNALLY,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils import (
    graph as g,
)
from utils.graph import (
    yield_dicts,
    yield_nodes,
)
from utils.model import (
    FindingEnum,
    Grammar,
    Vulnerability,
)
from zone import (
    t,
)


def _csharp_switch_no_default(
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
            defaults_count: int = sum(
                1
                for statement in switch[5:-1]
                for section in statement['Switch_section']
                if 'Switch_label' in section
                and section['Switch_label'][0]['text'] == 'default'
            )

            if defaults_count == 0:
                yield switch[0]['l'], switch[0]['c']

    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe={'478'},
        description=t(
            key='src.lib_path.f073.switch_no_default',
            path=path,
        ),
        finding=FindingEnum.F073,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def csharp_switch_no_default(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _csharp_switch_no_default,
        content=content,
        model=await parse_antlr(
            Grammar.CSHARP,
            content=content.encode(),
            path=path,
        ),
        path=path,
    )


def _java_switch_without_default(
    content: str,
    graph: nx.DiGraph,
    path: str,
) -> Tuple[Vulnerability, ...]:

    def iterator() -> Iterator[Dict[str, str]]:
        for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
            label_type='SwitchStatement',
        )):
            match = g.match_ast(graph, n_id, 'SwitchBlock')
            if c_id := match['SwitchBlock']:

                match = g.match_ast(graph, c_id, 'SwitchBlockStatementGroup')
                if c_id := match['SwitchBlockStatementGroup']:

                    default_ids = g.filter_nodes(
                        graph,
                        g.adj_ast(graph, c_id, depth=3),
                        g.pred_has_labels(label_type='DEFAULT'),
                    )

                    if len(default_ids) == 0:
                        yield graph.nodes[n_id]

    return blocking_get_vulnerabilities_from_n_attrs_iterator(
        content=content,
        cwe={'478'},
        description=t(
            key='src.lib_path.f073.switch_no_default',
            path=path,
        ),
        finding=FindingEnum.F073,
        n_attrs_iterator=iterator(),
        path=path,
    )


@CACHE_1SEC
@SHIELD
async def java_switch_without_default(
    content: str,
    graph: nx.DiGraph,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_switch_without_default,
        content=content,
        graph=graph,
        path=path,
    )


def _javascript_switch_no_default(
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
        cwe={'478'},
        description=t(
            key='src.lib_path.f073.switch_no_default',
            path=path,
        ),
        finding=FindingEnum.F073,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def javascript_switch_no_default(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _javascript_switch_no_default,
        content=content,
        model=await parse_babel(
            content=content.encode(),
            path=path,
        ),
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_CSHARP:
        coroutines.append(csharp_switch_no_default(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVA:
        content = await content_generator()
        graph = await java_parse_from_content(
            Grammar.JAVA9,
            content=content.encode(),
            path=path,
        )
        coroutines.append(java_switch_without_default(
            content=content,
            graph=graph,
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(javascript_switch_no_default(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
