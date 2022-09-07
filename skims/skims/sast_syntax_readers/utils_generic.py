# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    List,
    Tuple,
)
from utils import (
    graph as g,
)


def dependencies_from_arguments(
    args: SyntaxReaderArgs,
) -> List[graph_model.SyntaxSteps]:
    return [
        args.generic(args.fork_n_id(args_c_id))
        for args_c_id in g.adj_ast(args.graph, args.n_id)
        if args.graph.nodes[args_c_id]["label_type"]
        not in {
            ",",
            "(",
            ")",
            "{",
            "}",
        }
    ]


def get_dependencies_with_index(
    syntax_step_index: int,
    syntax_steps: graph_model.SyntaxSteps,
) -> List[Tuple[int, graph_model.SyntaxStep]]:
    dependencies: List[Tuple[int, graph_model.SyntaxStep]] = []
    dependencies_depth: int = 0
    dependencies_expected_length: int = -syntax_steps[
        syntax_step_index
    ].meta.dependencies

    while len(dependencies) < dependencies_expected_length:
        syntax_step_index -= 1

        if dependencies_depth:
            dependencies_depth += 1
        else:
            dependencies.append(
                (syntax_step_index, syntax_steps[syntax_step_index])
            )

        dependencies_depth += syntax_steps[syntax_step_index].meta.dependencies

    return dependencies


def get_dependencies(
    syntax_step_index: int,
    syntax_steps: graph_model.SyntaxSteps,
) -> graph_model.SyntaxSteps:
    return [
        step
        for _, step in get_dependencies_with_index(
            syntax_step_index, syntax_steps
        )
    ]
