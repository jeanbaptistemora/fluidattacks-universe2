from model.graph_model import (
    SyntaxStepCatchClause,
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
    # exceptions may not have an identifier
    if parameter_id := node_attrs.get("label_field_parameter"):
        yield SyntaxStepCatchClause(
            meta=SyntaxStepMeta.default(
                n_id=args.n_id,
                dependencies=dependencies_from_arguments(
                    args.fork_n_id(node_attrs["label_field_body"]),
                ),
            ),
            var=args.graph.nodes[parameter_id].get("label_text"),
        )
