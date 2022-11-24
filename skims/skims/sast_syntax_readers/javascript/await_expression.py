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
    yield from args.generic(
        args.fork_n_id(tuple(args.graph.adj[args.n_id].keys())[1])
    )
