# pylint: disable=too-many-lines
from __future__ import (
    annotations,
)

import contextlib
from model import (
    graph_model,
)
from sast_syntax_readers.dispatchers import (
    DISPATCHERS_BY_LANG,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    MissingSyntaxReader,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)
from utils.logs import (
    log_blocking,
)


def generic(
    args: SyntaxReaderArgs,
    *,
    warn_if_missing_syntax_reader: bool = True,
) -> graph_model.SyntaxSteps:
    n_attrs_label_type = args.graph.nodes[args.n_id]["label_type"]

    for _dispatcher in DISPATCHERS_BY_LANG[args.language]:
        if n_attrs_label_type in _dispatcher.applicable_node_label_types:
            try:
                return list(_dispatcher.syntax_reader(args))
            except MissingCaseHandling:
                continue

    if warn_if_missing_syntax_reader:
        log_blocking("debug", "Missing syntax reader for n_id: %s", args.n_id)

    raise MissingSyntaxReader(args)


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
                graph_syntax[n_id] = generic(
                    SyntaxReaderArgs(
                        generic=generic,
                        graph=graph,
                        language=language,
                        n_id=n_id,
                    ),
                    warn_if_missing_syntax_reader=False,
                )

    # Linearize items so we can evaluate steps in a linear for, no recursion
    for syntax_steps in graph_syntax.values():
        while linearize_syntax_steps(syntax_steps):
            # Nothing to assigned
            pass

    return graph_syntax
