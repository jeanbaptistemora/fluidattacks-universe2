from itertools import (
    chain,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def has_console_functions(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_HAS_CONSOLE_FUNCTIONS

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="member_access_expression"
                ),
            ):
                if node_to_str(shard.graph, member) == "Console.WriteLine":
                    pred_nid = g.pred_ast(shard.graph, member)[0]
                    args = g.get_ast_childs(
                        shard.graph, pred_nid, "argument", depth=2
                    )
                    args_childs = [
                        g.match_ast(shard.graph, arg).values() for arg in args
                    ]
                    parameters = [
                        shard.graph.nodes[arg]["label_type"]
                        for arg in filter(None, chain(*args_childs))
                    ]
                    if any(
                        param
                        in {"interpolated_string_expression", "identifier"}
                        for param in parameters
                    ):
                        yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f066.has_console_functions",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
