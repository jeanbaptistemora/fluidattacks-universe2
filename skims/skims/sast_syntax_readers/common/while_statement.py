from model.graph_model import (
    SyntaxStep,
    SyntaxStepLoop,
    SyntaxStepMeta,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    yield SyntaxStepLoop(
        meta=SyntaxStepMeta.default(
            args.n_id,
        ),
    )
