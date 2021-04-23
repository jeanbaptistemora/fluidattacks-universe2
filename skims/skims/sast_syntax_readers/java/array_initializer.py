# Local libraries
from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    # String[] a = {1,2}
    yield graph_model.SyntaxStepArrayInitialization(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            dependencies_from_arguments(args.fork_n_id(args.n_id)),
        )
    )
