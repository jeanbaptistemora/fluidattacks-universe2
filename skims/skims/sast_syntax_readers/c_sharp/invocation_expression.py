from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from utils import (
    graph as g,
)
from utils.graph.transformation import (
    get_base_identifier_id,
    node_to_str,
)
from utils.string import (
    split_on_first_dot,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    mem_access = "member_access_expression"

    match = g.match_ast(
        args.graph,
        args.n_id,
        "identifier",
        "argument_list",
        mem_access,
    )

    args_id = match["argument_list"]

    if not args_id:
        raise MissingCaseHandling(args)

    if _identifier := match["identifier"]:
        yield graph_model.SyntaxStepMethodInvocation(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                dependencies_from_arguments(
                    args.fork_n_id(args_id),
                ),
            ),
            method=args.graph.nodes[_identifier]["label_text"],
            current_instance=graph_model.CurrentInstance(fields={}),
        )
    elif member := match[mem_access]:
        base_ident = get_base_identifier_id(args.graph, member, mem_access)

        if not base_ident:
            raise MissingCaseHandling(args)

        _method_name = node_to_str(args.graph, member)
        _, method_name = split_on_first_dot(_method_name)
        yield graph_model.SyntaxStepMethodInvocationChain(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(base_ident)),
                    *dependencies_from_arguments(
                        args.fork_n_id(args_id),
                    ),
                ],
            ),
            method=method_name,
        )
    else:
        raise MissingCaseHandling(args)
