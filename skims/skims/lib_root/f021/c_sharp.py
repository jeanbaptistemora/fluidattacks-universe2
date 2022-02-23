from lib_root.utilities.c_sharp import (
    get_object_from_var,
    search_member_method_invocation,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)


def xpath_injection(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.SYMB_XPATH_INJECTION
    finding = method.value.finding
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            graph = shard.syntax_graph
            for n_id in search_method_invocation_naive(
                graph, {"SelectSingleNode"}
            ):
                if member := search_member_method_invocation(graph, n_id):
                    for path in get_backward_paths(graph, n_id):
                        if get_object_from_var(
                            shard, member, n_id
                        ) == "XPathNavigator" and evaluate(
                            c_sharp, finding, graph, path, n_id
                        ):
                            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f021.xpath_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
