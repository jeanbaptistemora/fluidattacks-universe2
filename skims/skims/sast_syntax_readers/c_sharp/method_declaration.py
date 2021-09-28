from model.graph_model import (
    SyntaxStepMeta,
    SyntaxStepMethodDeclaration,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    attrs = args.graph.nodes[args.n_id]
    name_id = attrs["label_field_name"]
    param_list_id = attrs["label_field_parameters"]

    yield SyntaxStepMethodDeclaration(
        meta=SyntaxStepMeta.default(
            args.n_id,
            dependencies_from_arguments(
                args.fork_n_id(param_list_id),
            ),
        ),
        name=args.graph.nodes[name_id]["label_text"],
    )
