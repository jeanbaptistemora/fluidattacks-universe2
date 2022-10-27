# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    CurrentInstance,
    SyntaxStep,
    SyntaxStepMeta,
    SyntaxStepMethodInvocation,
    SyntaxStepMethodInvocationChain,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from typing import (
    Iterator,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "identifier",
        "selector_expression",
        "argument_list",
    )

    args_id = match["argument_list"]
    if (func_id := match["identifier"]) and args_id:
        yield SyntaxStepMethodInvocation(
            meta=SyntaxStepMeta.default(
                args.n_id,
                dependencies_from_arguments(args.fork_n_id(args_id)),
            ),
            method=args.graph.nodes[func_id]["label_text"],
            current_instance=CurrentInstance(fields={}),
        )
    elif selector_id := match["selector_expression"]:
        match = g.match_ast(
            args.graph,
            selector_id,
            "identifier",
            "field_identifier",
            "call_expression",
        )

        field_id = match["field_identifier"]
        if field_id and (func_id := match["identifier"]):
            yield SyntaxStepMethodInvocation(
                meta=SyntaxStepMeta.default(
                    args.n_id,
                    dependencies_from_arguments(args.fork_n_id(str(args_id))),
                ),
                method=g.concatenate_label_text(
                    args.graph, (func_id, field_id), "."
                ),
                current_instance=CurrentInstance(fields={}),
            )
        elif field_id and (call_id := match["call_expression"]):
            yield SyntaxStepMethodInvocationChain(
                meta=SyntaxStepMeta.default(
                    args.n_id,
                    [
                        args.generic(args.fork_n_id(call_id)),
                        *dependencies_from_arguments(
                            args.fork_n_id(str(args_id))
                        ),
                    ],
                ),
                method=args.graph.nodes[field_id]["label_text"],
                current_instance=CurrentInstance(fields={}),
            )
        else:
            raise MissingCaseHandling(args)
    else:
        raise MissingCaseHandling(args)
