import itertools
from lib_root.utilities.c_sharp import (
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


def ldap_connections_authenticated(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    directory_object = {
        "DirectoryEntry",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        for shard, member in itertools.chain(
            yield_object_creation(graph_db, directory_object),
        ):
            arguments = g.get_ast_childs(
                shard.graph, member, "argument", depth=2
            )
            for arg in arguments:
                child = g.match_ast(
                    shard.graph, arg, "member_access_expression"
                )
                if child["member_access_expression"]:
                    test = node_to_str(
                        shard.graph,
                        child["member_access_expression"],
                    )
                    if test == "AuthenticationTypes.None":
                        yield shard, member

    return get_vulnerabilities_from_n_ids(
        cwe=("90",),
        desc_key="F320.title",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F320
