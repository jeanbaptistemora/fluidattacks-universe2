from model import (
    graph_model,
)
from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]

    arguments = []
    if identifier_id := node_attrs.get("label_field_parameter"):
        arguments.append(
            [
                SyntaxStepDeclaration(
                    meta=SyntaxStepMeta.default(args.n_id),
                    var=args.graph.nodes[identifier_id]["label_text"],
                )
            ]
        )
    elif parameters_id := node_attrs.get("label_field_parameters"):
        arguments.append(args.generic(args.fork_n_id(parameters_id)))

    yield graph_model.SyntaxStepLambdaExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            arguments,
        ),
    )
