# Standard library
from __future__ import (
    annotations,
)
import contextlib
from typing import (
    Callable,
    Dict,
    List,
    NamedTuple,
    Set,
    Tuple,
)

# Local libraries
from model import (
    graph_model,
)
from utils import (
    graph as g,
)
from utils.function import (
    get_id,
)
from utils.logs import (
    log_blocking,
)


class SyntaxReaderArgs(NamedTuple):
    graph: graph_model.Graph
    language: graph_model.GraphShardMetadataLanguage
    n_id: graph_model.NId

    def fork_n_id(self, n_id: graph_model.NId) -> SyntaxReaderArgs:
        return SyntaxReaderArgs(
            graph=self.graph,
            language=self.language,
            n_id=n_id,
        )


SyntaxReader = Callable[[SyntaxReaderArgs], graph_model.SyntaxStepsLazy]
SyntaxReaders = Tuple[SyntaxReader, ...]


class Dispatcher(NamedTuple):
    applicable_languages: Set[graph_model.GraphShardMetadataLanguage]
    applicable_node_label_types: Set[str]
    syntax_readers: SyntaxReaders


Dispatchers = Tuple[Dispatcher, ...]


class MissingSyntaxReader(Exception):
    pass


class MissingCaseHandling(Exception):

    def __init__(
        self,
        reader: SyntaxReader,
        reader_args: SyntaxReaderArgs,
    ) -> None:
        log_blocking(
            'debug', 'Missing case handling: %s, %s',
            get_id(reader), reader_args.n_id,
        )
        super().__init__()


def local_variable_declaration(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        'array_type',
        'scoped_type_identifier',
        'type_identifier',

        'variable_declarator',
    )

    if (
        (var_type_id := (
            match['array_type']
            or match['scoped_type_identifier']
            or match['type_identifier']
        ))
        and (var_decl_id := match['variable_declarator'])
    ):
        match = g.match_ast(
            args.graph,
            var_decl_id,
            'identifier',
            '=',
            '__0__',
        )

        if (
            (var_id := match['identifier'])
            and match['=']
            and (dependencies_id := match['__0__'])
        ):
            yield graph_model.SyntaxStepDeclaration(
                dependencies=[
                    generic(args.fork_n_id(dependencies_id)),
                ],
                meta=graph_model.SyntaxStepMeta.default(),
                var=args.graph.nodes[var_id]['label_text'],
                var_type=args.graph.nodes[var_type_id]['label_text'],
            )
        else:
            raise MissingCaseHandling(local_variable_declaration, args)
    else:
        raise MissingCaseHandling(local_variable_declaration, args)


def noop(_args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    yield graph_model.SyntaxStepNoOp(
        meta=graph_model.SyntaxStepMeta.default(),
    )


def method_declaration(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    for ps_id in g.get_ast_childs(args.graph, args.n_id, 'formal_parameters'):
        for p_id in g.get_ast_childs(args.graph, ps_id, 'formal_parameter'):
            yield from method_declaration_formal_parameter(
                args.fork_n_id(p_id)
            )


def method_declaration_formal_parameter(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, 'type_identifier', 'identifier')

    if (
        len(match) == 2
        and (var_type_id := match['type_identifier'])
        and (var_id := match['identifier'])
    ):
        yield graph_model.SyntaxStepDeclaration(
            dependencies=[],
            meta=graph_model.SyntaxStepMeta.default(),
            var=args.graph.nodes[var_id]['label_text'],
            var_type=args.graph.nodes[var_type_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(method_declaration_formal_parameter, args)


def method_invocation(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    c_ids = g.adj_ast(args.graph, args.n_id)

    identifier_ids = c_ids[0:-1]
    args_id = c_ids[-1]

    if g.contains_label_type_in(args.graph, identifier_ids, {
        'field_access',
        'identifier',
        '.',
    }):
        yield graph_model.SyntaxStepMethodInvocation(
            dependencies=dependencies_from_arguments(args.fork_n_id(args_id)),
            meta=graph_model.SyntaxStepMeta.default(),
            method=g.concatenate_label_text(args.graph, identifier_ids),
        )
    else:
        raise MissingCaseHandling(method_invocation, args)


def object_creation_expression(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, 'new', '__0__', 'argument_list')

    # pylint: disable=used-before-assignment
    if (
        len(match) == 3
        and match['new']
        and (object_type_id := match['__0__'])
        and (args_id := match['argument_list'])
        and (args.graph.nodes[object_type_id]['label_type'] in {
            'scoped_type_identifier',
        })
    ):
        yield graph_model.SyntaxStepObjectInstantiation(
            dependencies=dependencies_from_arguments(args.fork_n_id(args_id)),
            meta=graph_model.SyntaxStepMeta.default(),
            object_type=args.graph.nodes[object_type_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(method_invocation, args)


def string_literal(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    yield graph_model.SyntaxStepStringLiteral(
        meta=graph_model.SyntaxStepMeta.default(),
        value=args.graph.nodes[args.n_id]['label_text'][1:-1],
    )


def generic(
    args: SyntaxReaderArgs,
    *,
    warn_if_missing_syntax_reader: bool = True,
) -> graph_model.SyntaxSteps:
    n_attrs_label_type = args.graph.nodes[args.n_id]['label_type']
    for dispatcher in DISPATCHERS_BY_LANG[args.language]:
        if n_attrs_label_type in dispatcher.applicable_node_label_types:
            for syntax_reader in dispatcher.syntax_readers:
                try:
                    return list(syntax_reader(args))
                except MissingCaseHandling:
                    continue

    if warn_if_missing_syntax_reader:
        log_blocking('debug', 'Missing syntax reader for n_id: %s', args.n_id)

    raise MissingSyntaxReader(args)


def dependencies_from_arguments(
    args: SyntaxReaderArgs,
) -> List[graph_model.SyntaxSteps]:
    return [
        generic(args.fork_n_id(args_c_id))
        for args_c_id in g.adj_ast(args.graph, args.n_id)[1:-1]
        if args.graph.nodes[args_c_id]['label_type'] != ','
    ]


DISPATCHERS: Tuple[Dispatcher, ...] = (
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'local_variable_declaration',
        },
        syntax_readers=(
            local_variable_declaration,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'method_declaration',
        },
        syntax_readers=(
            method_declaration,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'method_invocation',
        },
        syntax_readers=(
            method_invocation,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'object_creation_expression',
        },
        syntax_readers=(
            object_creation_expression,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'string_literal',
        },
        syntax_readers=(
            string_literal,
        ),
    ),
    *[
        Dispatcher(
            applicable_languages={
                graph_model.GraphShardMetadataLanguage.JAVA,
            },
            applicable_node_label_types={
                applicable_node_label_type
            },
            syntax_readers=(
                noop,
            ),
        )
        for applicable_node_label_type in (
            'block',
            'comment',
            'expression_statement',
            ';',
        )
    ],
)
DISPATCHERS_BY_LANG: Dict[
    graph_model.GraphShardMetadataLanguage,
    Dispatchers,
] = {
    language: tuple(
        dispatcher
        for dispatcher in DISPATCHERS
        if language in dispatcher.applicable_languages
    )
    for language in graph_model.GraphShardMetadataLanguage
}


def read_from_graph(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> graph_model.GraphSyntax:
    graph_syntax: graph_model.GraphSyntax = {}

    # Read the syntax of every node in the graph, if possible
    for n_id in graph.nodes:
        if n_id not in graph_syntax:
            with contextlib.suppress(MissingSyntaxReader):
                graph_syntax[n_id] = generic(SyntaxReaderArgs(
                    graph=graph,
                    language=language,
                    n_id=n_id,
                ), warn_if_missing_syntax_reader=False)

    return graph_syntax
