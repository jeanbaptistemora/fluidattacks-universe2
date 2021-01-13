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
    in_process,
)

# Local libraries
from graph_java.get import (
    get as java_get_graph,
)
from parse_antlr.parse import (
    parse as parse_antlr,
)
from parse_babel import (
    parse as parse_babel,
)
from lib_path.common import (
    EXTENSIONS_CSHARP,
    EXTENSIONS_JAVA,
    EXTENSIONS_JAVASCRIPT,
    SHIELD,
    get_vulnerabilities_from_iterator_blocking,
    get_vulnerabilities_from_n_attrs_iterable_blocking,
)
from state.cache import (
    CACHE_1SEC,
    CACHE_ETERNALLY,
)
from utils import (
    graph as g,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from utils.graph import (
    yield_dicts,
    yield_nodes,
)
from model import (
    core_model,
    graph_model,
)
from zone import (
    t,
)


def _csharp_switch_no_default(
    content: str,
    model: Dict[str, Any],
    path: str,
) -> core_model.Vulnerabilities:

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

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={'478'},
        description=t(
            key='src.lib_path.f073.switch_no_default',
            path=path,
        ),
        finding=core_model.FindingEnum.F073,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def csharp_switch_no_default(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _csharp_switch_no_default,
        content=content,
        model=await parse_antlr(
            core_model.Grammar.CSHARP,
            content=content.encode(),
            path=path,
        ),
        path=path,
    )


def _java_switch_without_default(
    content: str,
    graph: graph_model.Graph,
    path: str,
) -> core_model.Vulnerabilities:

    def iterator() -> Iterator[Dict[str, str]]:
        for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
            label_type='SwitchStatement',
        )):
            match = g.match_ast(graph, n_id, 'SwitchBlock')
            if c_id := match['SwitchBlock']:
                default_ids = g.filter_nodes(
                    graph,
                    g.adj_ast(graph, c_id, depth=4),
                    g.pred_has_labels(label_type='DEFAULT'),
                )

                if len(default_ids) == 0:
                    yield graph.nodes[n_id]

    return get_vulnerabilities_from_n_attrs_iterable_blocking(
        content=content,
        cwe={'478'},
        description=t(
            key='src.lib_path.f073.switch_no_default',
            path=path,
        ),
        finding=core_model.FindingEnum.F073,
        n_attrs_iterable=tuple(iterator()),
        path=path,
    )


@CACHE_1SEC
@SHIELD
@TIMEOUT_1MIN
async def java_switch_without_default(
    content: str,
    graph: graph_model.Graph,
    path: str,
) -> core_model.Vulnerabilities:
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
) -> core_model.Vulnerabilities:

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

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={'478'},
        description=t(
            key='src.lib_path.f073.switch_no_default',
            path=path,
        ),
        finding=core_model.FindingEnum.F073,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def javascript_switch_no_default(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
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
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if file_extension in EXTENSIONS_CSHARP:
        coroutines.append(csharp_switch_no_default(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVA:
        content = await content_generator()
        graph = await java_get_graph(
            core_model.Grammar.JAVA9,
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

    return coroutines
