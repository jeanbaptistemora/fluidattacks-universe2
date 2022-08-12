from itertools import (
    chain,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    string,
)

POSSIBLE_METHODS = [
    ("System", "Text", "Encoding", "UTF7", "GetBytes"),
    ("System", "Text", "Encoding", "UTF8", "GetBytes"),
    ("System", "Text", "Encoding", "Unicode", "GetBytes"),
    ("System", "Text", "Encoding", "BigEndianUnicode", "GetBytes"),
    ("System", "Text", "Encoding", "UTF32", "GetBytes"),
]

DANGER_METHODS = set(
    chain.from_iterable(
        string.build_attr_paths(*method) for method in POSSIBLE_METHODS
    )
)


def cs_check_hashes_salt(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]["expression"]
    args.evaluation[args.n_id] = ma_attr in DANGER_METHODS
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
