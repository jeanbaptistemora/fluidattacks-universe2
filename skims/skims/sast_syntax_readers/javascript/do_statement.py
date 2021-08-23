from model.graph_model import (
    SyntaxStepLoop,
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
    yield SyntaxStepLoop(
        meta=SyntaxStepMeta.default(
            args.n_id,
            dependencies_from_arguments(
                args.fork_n_id(
                    args.graph.nodes[args.n_id]["label_field_condition"]
                ),
            ),
        ),
    )
