# Standard library
from typing import (
    List,
)

# Local libraries
from model import (
    graph_model,
)
from sast.syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def dependencies_from_arguments(
    args: SyntaxReaderArgs,
) -> List[graph_model.SyntaxSteps]:
    return [
        args.generic(args.fork_n_id(args_c_id))
        for args_c_id in g.adj_ast(args.graph, args.n_id)
        if args.graph.nodes[args_c_id]['label_type'] not in {
            ',',
            '(',
            ')',
            '{',
            '}',
        }
    ]
