# pylint: disable=too-many-lines
# Standard library
from __future__ import (
    annotations,
)
import contextlib
from typing import (
    Dict,
    Tuple,
)

# Local libraries
from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    Dispatcher,
    Dispatchers,
    MissingCaseHandling,
    MissingSyntaxReader,
    SyntaxReaderArgs,
)
from sast_syntax_readers.java import (
    array_access as java_array_access,
    array_creation_expression as java_array_creation_expression,
    array_initializer as java_array_initializer,
    assignment_expression as java_assignment_expression,
    binary_expression as java_binary_expression,
    cast_expression as java_cast_expression,
    catch_clause as java_catch_clause,
    enhanced_for_statement as java_enhanced_for_statement,
    for_statement as java_for_statement,
    identifier as java_identifier,
    if_statement as java_if_statement,
    instanceof_expression as java_instanceof_expression,
    literal as java_literal,
    local_variable_declaration as java_local_variable_declaration,
    method_declaration as java_method_declaration,
    method_invocation as java_method_invocation,
    object_creation_expression as java_object_creation_expression,
    parenthesized_expression as java_parenthesized_expression,
    resource as java_resource,
    return_statement as java_return_statement,
    switch_label as java_switch_label,
    switch_statement as java_switch_statement,
    ternary_expression as java_ternary_expression,
    unary_expression as java_unary_expression,
    while_statement as java_while_statement,
)
from utils import graph as g
from utils.logs import log_blocking


def noop(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    yield graph_model.SyntaxStepNoOp(
        meta=graph_model.SyntaxStepMeta.default(args.n_id),
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


DISPATCHERS: Tuple[Dispatcher, ...] = (
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            'assignment_expression',
        },
        syntax_readers=(
            java_assignment_expression.reader,
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
            java_ternary_expression.reader,
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
            java_binary_expression.reader,
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
            java_unary_expression.reader,
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
            java_enhanced_for_statement.reader,
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
            java_while_statement.reader,
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
            java_for_statement.reader,
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
            java_identifier.reader,
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
            java_if_statement.reader,
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
            java_parenthesized_expression.reader,
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
            java_cast_expression.reader,
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
            java_instanceof_expression.reader,
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
            java_catch_clause.reader,
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
            java_switch_statement.reader,
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
            java_switch_label.reader,
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
            java_local_variable_declaration.reader,
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
            java_method_declaration.reader,
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
            java_method_invocation.reader,
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
            java_array_access.reader,
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
            java_object_creation_expression.reader,
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
            java_array_creation_expression.reader,
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
            java_array_initializer.reader,
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
            java_literal.reader,
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
            java_resource.reader,
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
            java_return_statement.reader,
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
                    generic=generic,
                    graph=graph,
                    language=language,
                    n_id=n_id,
                ), warn_if_missing_syntax_reader=False)

    # Linearize items so we can evaluate steps in a linear for, no recursion
    for syntax_steps in graph_syntax.values():
        while linearize_syntax_steps(syntax_steps):
            pass

    return graph_syntax
