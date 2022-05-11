from lib_root.utilities.c_sharp import (
    check_member_acces_expression,
    yield_shard_member_access,
)
from lib_sast.types import (
    ShardDb,
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
from utils import (
    graph as g,
)


def insecure_assembly_load(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_ASSEMBLY_LOAD
    finding = method.value.finding
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            for member in yield_shard_member_access(shard, {"Assembly"}):
                if not check_member_acces_expression(shard, member, "Load"):
                    continue
                graph = shard.syntax_graph
                pred = g.pred_ast(shard.graph, member)[0]
                for path in get_backward_paths(graph, pred):
                    if (
                        evaluation := evaluate(
                            c_sharp, finding, graph, path, pred
                        )
                    ) and evaluation.danger:
                        yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f413.insecure_assembly_load",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
