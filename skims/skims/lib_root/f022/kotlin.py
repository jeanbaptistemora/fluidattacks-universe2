from lib_root.utilities.kotlin import (
    yield_method_invocation,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from sast_syntax_readers.kotlin.common import (
    get_composite_name,
)
from typing import (
    Set,
)
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)


def _kotlin_yield_unencrypted_channels(graph_db: GraphDB) -> GraphShardNodes:
    unencrypted_methods = complete_attrs_on_set(
        {
            "org.apache.commons.net.ftp.FTPClient",
            "org.apache.commons.net.smtp.SMTPClient",
            "org.apache.commons.net.telnet.TelnetClient",
        }
    )
    unsafe_methods = complete_attrs_on_set({"ConnectionSpec.Builder"})
    unsafe_protocol: Set[str] = {"CLEARTEXT"}
    for shard, method_id, method_name in yield_method_invocation(graph_db):
        if method_name in unencrypted_methods:
            yield shard, method_id
        if method_name in unsafe_methods:
            match = g.match_ast_group(
                shard.graph, method_id, "value_argument", depth=3
            )
            parameters = [
                g.adj_ast(shard.graph, argument_id)[0]
                for argument_id in match["value_argument"]
            ]
            if parameters:
                param_id = parameters[0]
                param_value = get_composite_name(
                    shard.graph, g.pred_ast(shard.graph, param_id)[0]
                )
                protocol = param_value.split(".")[-1]
                if protocol in unsafe_protocol:
                    yield shard, param_id


def unencrypted_channel(graph_db: GraphDB) -> Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("319"),
        desc_key="src.lib_path.f022.unencrypted_channel",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=_kotlin_yield_unencrypted_channels(graph_db),
    )


# Constants
FINDING: FindingEnum = FindingEnum.F022
