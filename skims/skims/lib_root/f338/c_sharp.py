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
from utils.graph.text_nodes import (
    node_to_str,
)
from utils.string import (
    build_attr_paths,
)


def check_hashes_salt(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    directory_object = {
        "Rfc2898DeriveBytes",
    }

    possible_methods = [
        ("System", "Text", "Encoding", "UTF7", "GetBytes"),
        ("System", "Text", "Encoding", "UTF8", "GetBytes"),
        ("System", "Text", "Encoding", "Unicode", "GetBytes"),
        ("System", "Text", "Encoding", "BigEndianUnicode", "GetBytes"),
        ("System", "Text", "Encoding", "UTF32", "GetBytes"),
    ]

    def n_ids() -> graph_model.GraphShardNodes:

        danger_methods = set(
            chain.from_iterable(
                build_attr_paths(*method) for method in possible_methods
            )
        )

        for shard, member in chain(
            yield_object_creation(graph_db, directory_object),
        ):
            parameters = g.get_ast_childs(
                shard.graph, member, "argument", depth=2
            )
            if len(parameters) > 1:
                node_param = g.match_ast(shard.graph, parameters[1])["__0__"]
                if (
                    shard.graph.nodes[node_param].get("label_type")
                    == "identifier"
                    and get_variable_attribute(
                        shard.graph,
                        shard.graph.nodes[node_param].get("label_text"),
                        "label_text",
                    )
                    in danger_methods
                ):
                    yield shard, member
                elif (
                    shard.graph.nodes[node_param].get("label_type")
                    == "invocation_expression"
                    and node_to_str(
                        shard.graph,
                        g.match_ast(shard.graph, node_param, "__0__")["__0__"],
                    )
                    in danger_methods
                ):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        cwe=("90",),
        desc_key="F338.title",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F338
