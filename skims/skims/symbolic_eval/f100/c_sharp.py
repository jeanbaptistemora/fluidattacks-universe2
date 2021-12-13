from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
    search_method_invocation,
)


def analyze(graph: Graph) -> None:
    finding = FindingEnum.F100
    language = GraphLanguage.CSHARP

    for n_id in search_method_invocation(graph, {"Create"}):
        for path in get_backward_paths(graph, n_id):
            if evaluate(language, finding, graph, path, n_id):
                print(path, n_id)

    print("Finished")
