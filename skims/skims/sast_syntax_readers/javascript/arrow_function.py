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
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]

    if identifier_id := node_attrs.get("label_field_parameter"):
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(args.n_id),
            var=args.graph.nodes[identifier_id]["label_text"],
        )
    elif parameters_id := node_attrs.get("label_field_parameters"):
        yield from args.generic(args.fork_n_id(parameters_id))

    yield graph_model.SyntaxStepLambdaExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            dependencies_from_arguments(
                args.fork_n_id(node_attrs.get("label_field_body"))
            ),
        ),
    )
