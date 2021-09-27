import itertools
from lib_root.utilities.c_sharp import (
    get_variable_attribute,
    yield_object_creation,
)
from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
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
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        regex_methods = {"IsMatch", "Match", "Matches"}
        for shard, node in itertools.chain(
            yield_object_creation(
                graph_db,
                {
                    "Regex",
                },
            ),
        ):
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
                    if regex_param:
                        yield shard, invocation
                    elif var_param and vuln_attributes(shard.graph, var_param):
                        yield shard, invocation

    def vuln_attributes(
        graph: graph_model.GraphShard,
        list_vars: Tuple[str, ...],
    ) -> bool:
        for node_var in list_vars:
            var_name = graph.nodes[node_var].get("label_text")
            if (
                get_variable_attribute(
                    graph,
                    var_name,
                    "label_type",
                )
                == "verbatim_string_literal"
            ):
                return True
        return False

    return get_vulnerabilities_from_n_ids(
        cwe=("405",),
        desc_key="F211.title",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F211
