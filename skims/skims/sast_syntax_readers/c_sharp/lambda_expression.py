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


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    if "label_field_body" not in node_attrs:
        raise MissingCaseHandling(args)

    identifier = g.match_ast_d(args.graph, args.n_id, "identifier")
    params = g.match_ast_d(args.graph, args.n_id, "parameter_list")

    yield graph_model.SyntaxStepLambdaExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            # if there is only one parameter it is directly represented as
            # an identifier so the syntax step needs to be made by hand
            dependencies=[
                [
                    graph_model.SyntaxStepDeclaration(
                        meta=graph_model.SyntaxStepMeta.default(identifier),
                        var=args.graph.nodes[identifier]["label_text"],
                        var_type=None,
                    )
                ]
            ]
            if params is None
            else dependencies_from_arguments(args.fork_n_id(params)),
        ),
    )
