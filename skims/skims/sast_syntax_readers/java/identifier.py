# Local libraries
from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    yield graph_model.SyntaxStepSymbolLookup(
        meta=graph_model.SyntaxStepMeta.default(args.n_id),
        symbol=args.graph.nodes[args.n_id]['label_text'],
    )
