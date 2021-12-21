from model.core_model import (
    FindingEnum,
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
    finding = FindingEnum.F100
    language = GraphLanguage.CSHARP
    graph = shard.syntax_graph
    src_method = "symbolic.f100.c_sharp"

    for n_id in search_method_invocation(graph, {"Create"}):
        for path in get_backward_paths(graph, n_id):
            if evaluate(language, finding, graph, path, n_id):
                yield create_vulnerability(finding, shard, n_id, src_method)
