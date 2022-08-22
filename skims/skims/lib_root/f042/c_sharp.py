from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
    yield_syntax_graph_object_creation,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
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
from utils import (
    graph as g,
)


def insecurely_generated_cookies(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_INSEC_COOKIES
    object_name = {"HttpCookie"}
    security_props = {
        "HttpOnly",
        "Secure",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for object_nid in yield_syntax_graph_object_creation(
                graph, object_name
            ):
                insecure = False
                sec_access = []
                pred = g.pred(graph, object_nid)[0]
                var = {graph.nodes[pred].get("variable")}

                for nid in yield_syntax_graph_member_access(graph, var):
                    if graph.nodes[nid].get("member") not in security_props:
                        continue
                    test_nid = graph.nodes[g.pred(graph, nid)[0]].get(
                        "value_id"
                    )
                    sec_access.append(nid)
                    for path in get_backward_paths(graph, test_nid):
                        evaluation = evaluate(method, graph, path, test_nid)
                        if evaluation and evaluation.danger:
                            insecure = True
                if insecure or len(sec_access) < 2:
                    yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.042.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
