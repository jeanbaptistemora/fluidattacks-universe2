# pylint: disable=too-many-lines
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
from model import graph_model
from utils import graph as g
from utils.logs import log_blocking
from utils.function import get_id


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


def assignment_expression(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    assignment_operators = {
        '=',
        '+=',
        '-=',
        '*=',
        '/=',
        '%=',
        '&=',
        '^=',
        '|=',
        '<<=',
        '>>=',
        '>>>=',
    }
    match = g.match_ast(
        args.graph,
        args.n_id,
        '__0__',
        '__1__',
        '__2__',
    )

    # pylint: disable=used-before-assignment
    if (
        (var_id := match['__0__'])
        and (op_id := match['__1__'])
        and (args.graph.nodes[op_id]['label_text'] in assignment_operators)
        and (src_id := match['__2__'])
    ):
        yield graph_model.SyntaxStepAssignment(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, [
                generic(args.fork_n_id(src_id)),
            ]),
            var=args.graph.nodes[var_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(assignment_expression, args)


def ternary_expression(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph, args.n_id, '__0__', '?', '__1__', ':', '__2__',
    )

    yield graph_model.SyntaxStepTernary(
        meta=graph_model.SyntaxStepMeta.default(args.n_id, [
            generic(args.fork_n_id(match['__2__'])),
            generic(args.fork_n_id(match['__1__'])),
            generic(args.fork_n_id(match['__0__'])),
        ]),
    )


def binary_expression(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    l_id, op_id, r_id = g.adj_ast(args.graph, args.n_id)

    yield graph_model.SyntaxStepBinaryExpression(
        meta=graph_model.SyntaxStepMeta.default(args.n_id, [
            generic(args.fork_n_id(r_id)),
            generic(args.fork_n_id(l_id)),
        ]),
        operator=args.graph.nodes[op_id]['label_text'],
    )


def switch_statement(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    # switch parenthesized_expression switch_block
    switch_c_ids = g.adj_ast(args.graph, args.n_id)
    switch_pred_id = switch_c_ids[1]
    switch_block_id = switch_c_ids[2]
    switch_label_ids = tuple(
        c_id
        for c_id in g.adj_ast(args.graph, switch_block_id)[1:-1]
        if args.graph.nodes[c_id]['label_type'] == 'switch_label'
    )

    yield graph_model.SyntaxStepSwitch(
        meta=graph_model.SyntaxStepMeta.default(args.n_id, [
            generic(args.fork_n_id(switch_label_id))
            for switch_label_id in reversed(switch_label_ids)
        ] + [
            generic(args.fork_n_id(switch_pred_id)),
        ]),
    )


def switch_label(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id)

    if len(match) == 3:
        yield graph_model.SyntaxStepSwitchLabelCase(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, [
                generic(args.fork_n_id(match['__1__'])),
            ]),
        )
    elif len(match) == 2:
        yield graph_model.SyntaxStepSwitchLabelDefault(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
        )
    else:
        raise MissingCaseHandling(switch_label, args)


def unary_expression(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    op_id, exp_id = g.adj_ast(args.graph, args.n_id)

    yield graph_model.SyntaxStepUnaryExpression(
        meta=graph_model.SyntaxStepMeta.default(args.n_id, [
            generic(args.fork_n_id(exp_id)),
        ]),
        operator=args.graph.nodes[op_id]['label_text'],
    )


def for_statement(args: SyntaxReaderArgs,) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph, args.n_id,
        'for',
        '(',
        'binary_expression',
        'local_variable_declaration',
        'update_expression',
        ')',
        'block',
    )
    if (
        len(match) == 8
        and (var := match['local_variable_declaration'])
        and (binary := match['binary_expression'])
        and (update := match['update_expression'])
    ):
        yield graph_model.SyntaxStepFor(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, [
                generic(args.fork_n_id(var)),
            ]),
            n_id_var_declaration=var,
            n_id_conditional_expression=binary,
            n_id_update=update,
        )
    else:
        raise MissingCaseHandling(for_statement, args)


def while_statement(args: SyntaxReaderArgs,) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph, args.n_id,
        'while',
        'parenthesized_expression',
        'block',
    )
    if (
        len(match) == 3
        and (expression := match['parenthesized_expression'])
    ):
        yield graph_model.SyntaxStepParenthesizedExpression(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id, dependencies_from_arguments(
                    args.fork_n_id(expression),
                ),
            ),
        )
    else:
        raise MissingCaseHandling(for_statement, args)


def enhanced_for_statement(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    # for (type foo: bar) { ... }
    match = g.match_ast(
        args.graph, args.n_id,
        'for',
        '(',
        '__0__',
        '__1__',
        ':',
        '__2__',
        ')',
        'block',
    )

    if (
        len(match) == 8
        and (var_type_id := match['__0__'])
        and (var_id := match['__1__'])
        and (src_id := match['__2__'])
    ):
        yield graph_model.SyntaxStepDeclaration(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, [
                generic(args.fork_n_id(src_id)),
            ]),
            var=args.graph.nodes[var_id]['label_text'],
            var_type=args.graph.nodes[var_type_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(enhanced_for_statement, args)


def identifier(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    yield graph_model.SyntaxStepSymbolLookup(
        meta=graph_model.SyntaxStepMeta.default(args.n_id),
        symbol=args.graph.nodes[args.n_id]['label_text'],
    )


def array_access(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, '__0__', '__2__')

    if (
        (n_id_object := match['__0__'])
        and (n_id_index := match['__2__'])
    ):
        yield graph_model.SyntaxStepArrayAccess(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, [
                generic(args.fork_n_id(n_id_object)),
                generic(args.fork_n_id(n_id_index)),
            ]),
        )
    else:
        raise MissingCaseHandling(array_access, args)


def array_creation_expression(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        'new',
        '__0__',
        'dimensions_expr',
    )

    if (
        len(match) == 3
        and match['new']
        and (object_type_id := match['__0__'])
        and (dimension := match['dimensions_expr'])
    ):
        match = g.match_ast(
            args.graph,
            dimension,
            '__1__',
        )
        yield graph_model.SyntaxStepArrayInstantiation(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id, dependencies_from_arguments(
                    args.fork_n_id(match['__1__']),
                ),
            ),
            array_type=args.graph.nodes[object_type_id]['label_text'],
        )
    elif (
        len(match) == 5
        and match['new']
        and (object_type_id := match['__0__'])
        and (match['__1__'])
        and (initializer := match['__2__'])
    ):
        yield graph_model.SyntaxStepArrayInstantiation(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, [
                generic(args.fork_n_id(initializer)),
            ]),
            array_type=args.graph.nodes[object_type_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(array_creation_expression, args)


def array_initializer(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    # String[] a = {1,2}
    yield graph_model.SyntaxStepArrayInitialization(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            dependencies_from_arguments(args.fork_n_id(args.n_id)),
        ))


def if_statement(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    # if ( __0__ ) __1__ else __2__
    match = g.match_ast(
        args.graph, args.n_id,
        'if',
        '__0__',
        '__1__',
        'else',
        '__2__',
    )

    n_id_false = match['__2__']
    if not n_id_false:
        # Read the else branch by following the CFG, if such branch exists
        c_ids = g.adj_cfg(args.graph, args.n_id)
        if len(c_ids) >= 2:
            n_id_false = c_ids[1]

    yield graph_model.SyntaxStepIf(
        meta=graph_model.SyntaxStepMeta.default(
            n_id=args.n_id,
            dependencies=dependencies_from_arguments(
                args.fork_n_id(match['__0__']),
            ),
        ),
        n_id_false=n_id_false,
        n_id_true=match['__1__'],
    )


def resource(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        '__0__',
        'identifier',
        '=',
        '__1__',
    )

    if (
        (var_type_id := match['__0__'])
        and (var_id := match['identifier'])
        and (var_src_id := match['__1__'])
    ):
        yield graph_model.SyntaxStepDeclaration(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, [
                generic(args.fork_n_id(var_src_id)),
            ]),
            var=args.graph.nodes[var_id]['label_text'],
            var_type=args.graph.nodes[var_type_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(resource, args)


def return_statement(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    return_id = g.adj_ast(args.graph, args.n_id)[1]

    yield graph_model.SyntaxStepReturn(
        meta=graph_model.SyntaxStepMeta.default(args.n_id, [
            generic(args.fork_n_id(return_id)),
        ]),
    )


def cast_expression(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        'type_identifier',
        'scoped_type_identifier',
        '(',
        ')',
        '__0__',
    )
    type_cast_id = match['type_identifier'] or match['scoped_type_identifier']
    if (len(match) == 5 and (statement := match['__0__'])):
        yield graph_model.SyntaxStepCastExpression(
            meta=graph_model.SyntaxStepMeta.default(
                n_id=args.n_id,
                dependencies=[
                    generic(args.fork_n_id(statement)),
                ],
            ),
            cast_type=args.graph.nodes[type_cast_id]['label_text']
        )
    else:
        raise MissingCaseHandling(cast_expression, args)


def instanceof_expression(
        args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        'type_identifier',
        'instanceof',
        'scoped_type_identifier',
        '__0__',
    )
    type_of_id = match['type_identifier'] or match['scoped_type_identifier']

    if (len(match) == 4 and (statement := match['__0__'])):
        yield graph_model.SyntaxStepInstanceofExpression(
            meta=graph_model.SyntaxStepMeta.default(
                n_id=args.n_id,
                dependencies=[
                    generic(args.fork_n_id(statement)),
                ],
            ),
            instanceof_type=args.graph.nodes[type_of_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(instanceof_expression, args)


def parenthesized_expression(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph, args.n_id,
        'type_identifier',
        '(',
        ')',
        '__0__',
    )
    yield graph_model.SyntaxStepParenthesizedExpression(
        meta=graph_model.SyntaxStepMeta.default(
            n_id=args.n_id,
            dependencies=[
                generic(args.fork_n_id(match['__0__'])),
            ],
        ),
    )


def catch_clause(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph, args.n_id,
        'catch',
        'catch_formal_parameter',
        'block',
    )
    if (
        len(match) == 5
        and (parameter := match['catch_formal_parameter'])
        and (block := match['block'])
    ):
        match = g.match_ast(
            args.graph,
            parameter,
            'catch_type',
            'identifier',
        )
        match_type = g.match_ast(
            args.graph,
            match['catch_type'],
            '__0__',
        )
        yield graph_model.SyntaxStepCatchClause(
            meta=graph_model.SyntaxStepMeta.default(
                n_id=args.n_id,
                dependencies=dependencies_from_arguments(
                    args.fork_n_id(block),
                ),
            ),
            var=args.graph.nodes[match['identifier']]['label_text'],
            catch_type=match_type['__0__'],
        )
    else:
        raise MissingCaseHandling(catch_clause, args)


def local_variable_declaration(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, '__0__', 'variable_declarator')

    if (
        (var_type_id := match['__0__']) and
        (var_decl_id := match['variable_declarator'])
    ):
        match = g.match_ast(args.graph, var_decl_id, '__0__', '=', '__1__')

        if var_id := match['__0__']:
            if match['='] and (deps_id := match['__1__']):
                deps_src = [generic(args.fork_n_id(deps_id))]
            else:
                deps_src = []

            yield graph_model.SyntaxStepDeclaration(
                meta=graph_model.SyntaxStepMeta.default(args.n_id, deps_src),
                var=args.graph.nodes[var_id]['label_text'],
                var_type=(
                    args.graph.nodes[var_type_id]['label_text']
                    .split('<', maxsplit=1)[0]
                ),
            )
        else:
            raise MissingCaseHandling(local_variable_declaration, args)
    else:
        raise MissingCaseHandling(local_variable_declaration, args)


def noop(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    yield graph_model.SyntaxStepNoOp(
        meta=graph_model.SyntaxStepMeta.default(args.n_id),
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
    match = g.match_ast(args.graph, args.n_id, '__0__', '__1__')

    if (
        len(match) == 2
        and (var_type_id := match['__0__'])
        and (var_id := match['__1__'])
    ):
        yield graph_model.SyntaxStepDeclaration(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            var=args.graph.nodes[var_id]['label_text'],
            var_type=args.graph.nodes[var_type_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(method_declaration_formal_parameter, args)


def method_invocation(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    c_ids = g.adj_ast(args.graph, args.n_id)

    identifier_ids = c_ids[0:-1]
    root_id = c_ids[0]
    path_ids = c_ids[1:-1]
    args_id = c_ids[-1]

    dot_chain = {
        'field_access',
        'identifier',
        '.',
    }

    if g.contains_label_type_in(args.graph, identifier_ids, dot_chain):
        yield graph_model.SyntaxStepMethodInvocation(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id, dependencies_from_arguments(
                    args.fork_n_id(args_id),
                ),
            ),
            method=g.concatenate_label_text(args.graph, identifier_ids),
        )
    elif g.contains_label_type_in(args.graph, path_ids, dot_chain):
        yield graph_model.SyntaxStepMethodInvocationChain(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id, [
                    generic(args.fork_n_id(root_id)),
                    *dependencies_from_arguments(
                        args.fork_n_id(args_id),
                    ),
                ],
            ),
            method=g.concatenate_label_text(args.graph, path_ids),
        )
    else:
        raise MissingCaseHandling(method_invocation, args)


def object_creation_expression(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, 'new', '__0__', 'argument_list')

    if (
        match['new']
        and (object_type_id := match['__0__'])
        and (args_id := match['argument_list'])
    ):
        yield graph_model.SyntaxStepObjectInstantiation(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id, dependencies_from_arguments(
                    args.fork_n_id(args_id),
                ),
            ),
            object_type=(
                args.graph.nodes[object_type_id]['label_text']
                .split('<', maxsplit=1)[0]
            ),
        )
    else:
        raise MissingCaseHandling(object_creation_expression, args)


def literal(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    n_attrs = args.graph.nodes[args.n_id]
    n_attrs_label_type = n_attrs['label_type']

    if n_attrs_label_type == 'decimal_integer_literal':
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs['label_text'],
            value_type='number',
        )
    elif n_attrs_label_type in {'false', 'true'}:
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs['label_text'],
            value_type='boolean',
        )
    elif n_attrs_label_type == 'null_literal':
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs['label_text'],
            value_type='null',
        )
    elif n_attrs_label_type in {'character_literal', 'string_literal'}:
        yield graph_model.SyntaxStepLiteral(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            value=n_attrs['label_text'][1:-1],
            value_type='string',
        )
    else:
        raise MissingCaseHandling(literal, args)


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
        for args_c_id in g.adj_ast(args.graph, args.n_id)
        if args.graph.nodes[args_c_id]['label_type'] not in {
            ',',
            '(',
            ')',
            '{',
            '}',
        }
    ]


DISPATCHERS: Tuple[Dispatcher, ...] = (
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'assignment_expression',
        },
        syntax_readers=(
            assignment_expression,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'ternary_expression',
        },
        syntax_readers=(
            ternary_expression,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'binary_expression',
        },
        syntax_readers=(
            binary_expression,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'unary_expression',
        },
        syntax_readers=(
            unary_expression,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'enhanced_for_statement',
        },
        syntax_readers=(
            enhanced_for_statement,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'while_statement',
        },
        syntax_readers=(
            while_statement,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'for_statement'
        },
        syntax_readers=(
            for_statement,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'field_access',
            'identifier',
        },
        syntax_readers=(
            identifier,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'if_statement',
        },
        syntax_readers=(
            if_statement,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'parenthesized_expression',
        },
        syntax_readers=(
            parenthesized_expression,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'cast_expression',
        },
        syntax_readers=(
            cast_expression,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'instanceof_expression',
        },
        syntax_readers=(
            instanceof_expression,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'catch_clause',
        },
        syntax_readers=(
            catch_clause,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'switch_statement',
        },
        syntax_readers=(
            switch_statement,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'switch_label',
        },
        syntax_readers=(
            switch_label,
        ),
    ),
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
            'array_access',
        },
        syntax_readers=(
            array_access,
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
            'array_creation_expression',
        },
        syntax_readers=(
            array_creation_expression,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'array_initializer',
        },
        syntax_readers=(
            array_initializer,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'character_literal',
            'decimal_integer_literal',
            'false',
            'floating_point_type',
            'null_literal',
            'string_literal',
            'true',
        },
        syntax_readers=(
            literal,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'resource',
        },
        syntax_readers=(
            resource,
        ),
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'return_statement',
        },
        syntax_readers=(
            return_statement,
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
            'break_statement',
            'class_body',
            'continue_statement',
            'comment',
            'expression_statement',
            'finally_clause',
            'resource_specification',
            'this',
            'try_statement',
            'try_with_resources_statement',
            'throw_statement',
            ';',
            '-',
            '+',
            '*',
            '/',
            '%',
            '(',
            ')',
            '.',
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


def linearize_syntax_steps(
    syntax_steps: graph_model.SyntaxSteps,
) -> bool:
    continue_linearizing: bool = False
    syntax_step_index = -1

    for syntax_step in syntax_steps.copy():
        syntax_step_index += 1

        if not syntax_step.meta.linear():
            stack = 0
            for dependency_syntax_steps in syntax_step.meta.dependencies:
                for dependency_syntax_step in reversed(
                    dependency_syntax_steps,
                ):
                    continue_linearizing = (
                        continue_linearizing
                        or not dependency_syntax_step.meta.linear()
                    )
                    syntax_steps.insert(
                        syntax_step_index,
                        dependency_syntax_step,
                    )
                    syntax_step_index += 1
                    stack += 1

            syntax_step.meta.dependencies = -1 * stack

    return continue_linearizing


def read_from_graph(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> graph_model.GraphSyntax:
    graph_syntax: graph_model.GraphSyntax = {}

    # Read the syntax of every node in the graph, if possible
    for n_id in graph.nodes:
        if n_id not in graph_syntax and g.is_connected_to_cfg(graph, n_id):
            with contextlib.suppress(MissingSyntaxReader):
                graph_syntax[n_id] = generic(SyntaxReaderArgs(
                    graph=graph,
                    language=language,
                    n_id=n_id,
                ), warn_if_missing_syntax_reader=False)

    # Linearize items so we can evaluate steps in a linear for, no recursion
    for syntax_steps in graph_syntax.values():
        while linearize_syntax_steps(syntax_steps):
            pass

    return graph_syntax
