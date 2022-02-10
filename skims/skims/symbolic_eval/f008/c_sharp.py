from model.core_model import (
    MethodsEnum,
    Vulnerability,
)
from model.graph_model import (
    GraphShard,
    GraphShardMetadataLanguage as GraphLanguage,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
    search_method_invocation,
)
from symbolic_eval.vulnerabilities import (
    create_vulnerability,
)
from typing import (
    Iterator,
)


def analyze(shard: GraphShard) -> Iterator[Vulnerability]:
    method = MethodsEnum.SYMB_INSEC_ADDHEADER_WRITE
    language = GraphLanguage.CSHARP
    graph = shard.syntax_graph

    for n_id in search_method_invocation(graph, {"AddHeader", "Write"}):
        for path in get_backward_paths(graph, n_id):
            if evaluate(language, method.value.finding, graph, path, n_id):
                yield create_vulnerability(shard, n_id, method)
