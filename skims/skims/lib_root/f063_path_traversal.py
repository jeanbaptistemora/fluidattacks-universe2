# Local libraries
from lib_root.common import (
    get_vulnerabilities_from_n_ids,
)
from model import (
    core_model,
    graph_model,
)
from sast.symeval import (
    from_untrusted_node_to_dangerous_action_node,
)


def query_from_untrusted_node_to_dangerous_action_node(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=('22',),
        desc_key='src.lib_path.f063_path_traversal.description',
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=from_untrusted_node_to_dangerous_action_node(
            graph_db,
            untrusted_node=core_model.FindingEnum.F063_PATH_TRAVERSAL,
        ),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F063_PATH_TRAVERSAL
QUERIES: graph_model.Queries = (
    query_from_untrusted_node_to_dangerous_action_node,
)
