from lib_root.utilities.c_sharp import (
    check_member_acces_expression,
    get_variable_attribute,
    yield_shard_member_access,
    yield_shard_object_creation,
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
from typing import (
    Tuple,
)
from utils import (
    graph as g,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def vuln_regular_expression(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):

            regex_methods = {"IsMatch", "Match", "Matches"}

            for node in yield_shard_object_creation(shard, {"Regex"}):
                _object = g.match_ast(
                    shard.graph, g.pred_ast(shard.graph, node, depth=2)[1]
                )["__0__"]
                name_object = shard.graph.nodes[_object].get("label_text")
                for member in g.filter_nodes(
                    shard.graph,
                    nodes=shard.graph.nodes,
                    predicate=g.pred_has_labels(
                        label_type="member_access_expression"
                    ),
                ):
                    expression = node_to_str(shard.graph, member).split(".")
                    if (
                        expression[0] == name_object
                        and expression[1] in regex_methods
                    ):
                        invocation = g.pred_ast(shard.graph, member)[0]
                        regex_param = g.get_ast_childs(
                            shard.graph,
                            invocation,
                            "verbatim_string_literal",
                            depth=3,
                        )
                        var_param = g.get_ast_childs(
                            shard.graph, invocation, "identifier", depth=3
                        )
                        if regex_param or (
                            var_param and vuln_attributes(shard, var_param)
                        ):
                            yield shard, invocation

    def vuln_attributes(
        shard: graph_model.GraphShard,
        list_vars: Tuple[str, ...],
    ) -> bool:
        for node_var in list_vars:
            var_name = shard.graph.nodes[node_var].get("label_text")
            if (
                get_variable_attribute(
                    shard,
                    var_name,
                    "type",
                )
                == "verbatim_string_literal"
            ):
                return True
        return False

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_vulnerable",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_VULN_REGEX,
    )


def regex_injection(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_REGEX_INJETCION
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP

    def n_ids() -> graph_model.GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            for member in yield_shard_member_access(shard, {"Regex"}):
                if not check_member_acces_expression(shard, member, "Match"):
                    continue
                graph = shard.syntax_graph
                pred = g.pred_ast(shard.graph, member)[0]
                for path in get_backward_paths(graph, pred):
                    if (
                        evaluation := evaluate(method, graph, path, pred)
                    ) and evaluation.danger:
                        yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
