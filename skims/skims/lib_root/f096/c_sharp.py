from itertools import (
    chain,
)
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
from utils import (
    graph as g,
)


def insecure_deserialization(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    danger_objects = {
        "BinaryFormatter",
        "LosFormatter",
    }

    def n_ids() -> graph_model.GraphShardNodes:

        for shard, member in chain(
            yield_object_creation(graph_db, danger_objects),
        ):
            obj_name = shard.graph.nodes[
                g.match_ast(shard.graph, member)["__1__"]
            ].get("label_text")
            if obj_name == "BinaryFormatter":
                yield shard, member
            elif obj_name == "LosFormatter":
                arg_node = g.get_ast_childs(
                    shard.graph, member, "argument", depth=2
                )[0]
                arg_type = shard.graph.nodes[
                    g.match_ast(shard.graph, arg_node)["__0__"]
                ].get("label_type")
                if (
                    arg_type == "boolean_literal"
                    and shard.graph.nodes[
                        g.match_ast(shard.graph, arg_node)["__0__"]
                    ].get("label_text")
                    == "false"
                ):
                    yield shard, member
                elif (
                    arg_type == "identifier"
                    and get_variable_attribute(
                        shard.graph,
                        shard.graph.nodes[
                            g.match_ast(shard.graph, arg_node)["__0__"]
                        ].get("label_text"),
                        "label_text",
                    )
                    == "false"
                ):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        cwe=("502",),
        desc_key="F096.title",
        desc_params={},
        finding=core_model.FindingEnum.F096,
        graph_shard_nodes=n_ids(),
    )
