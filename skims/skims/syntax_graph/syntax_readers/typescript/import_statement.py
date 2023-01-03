from model.graph_model import (
    NId,
)
from syntax_graph.syntax_readers.common.import_statement import (
    js_ts_reader,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    return js_ts_reader(args)
