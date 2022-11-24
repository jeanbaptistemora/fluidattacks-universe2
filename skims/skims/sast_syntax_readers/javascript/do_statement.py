from model.graph_model import (
    SyntaxStep,
    SyntaxStepLoop,
    SyntaxStepMeta,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from typing import (
    Iterator,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
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
