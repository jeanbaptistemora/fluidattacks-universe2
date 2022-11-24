from model import (
    graph_model,
)
from model.graph_model import (
    SyntaxStep,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    yield graph_model.SyntaxStepSwitchLabelDefault(
        meta=graph_model.SyntaxStepMeta.default(args.n_id),
    )
