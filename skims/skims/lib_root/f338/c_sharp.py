from itertools import (
    chain,
)
from lib_root.utilities.c_sharp import (
    get_variable_attribute,
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
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP

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

    danger_methods = set(
        chain.from_iterable(
            build_attr_paths(*method) for method in possible_methods
        )
    )

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            for member in yield_shard_object_creation(shard, directory_object):
                parameters = g.get_ast_childs(
                    shard.graph, member, "argument", depth=2
                )
                node_param = (
                    g.match_ast(shard.graph, parameters[1])["__0__"]
                    if len(parameters) > 1
                    else None
                )
                if (
                    shard.graph.nodes[node_param].get("label_type")
                    == "identifier"
                ):
                    var_assign = get_variable_attribute(
                        shard,
                        shard.graph.nodes[node_param].get("label_text"),
                        "text",
                    )
                    if (
                        var_assign
                        and var_assign.split("(")[0] in danger_methods
                    ):
                        yield shard, member
                elif (
                    shard.graph.nodes[node_param].get("label_type")
                    == "invocation_expression"
                    and node_to_str(
                        shard.graph,
                        str(
                            g.match_ast(shard.graph, str(node_param), "__0__")[
                                "__0__"
                            ]
                        ),
                    )
                    in danger_methods
                ):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.338.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_CHECK_HASHES_SALT,
    )
