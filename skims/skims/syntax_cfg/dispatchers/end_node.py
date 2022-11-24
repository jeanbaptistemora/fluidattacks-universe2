from model.graph_model import (
    NId,
)
from syntax_cfg.types import (
    SyntaxCfgArgs,
)


def build(args: SyntaxCfgArgs) -> NId:
    return args.n_id
