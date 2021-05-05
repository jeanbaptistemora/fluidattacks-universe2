# Local libraries
from sast.query import get_vulnerabilities_from_n_ids
from utils import (
    graph as g,
)
from model import (
    core_model,
    graph_model,
)


def csharp_insecure_hash(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    insecure_cyphers = {
        "HMACMD5",
        "HMACRIPEMD160",
        "HMACSHA1",
        "MACTripleDES",
        "MD5",
        "MD5Cng",
        "MD5CryptoServiceProvider",
        "MD5Managed",
        "RIPEMD160",
        "RIPEMD160Managed",
        "SHA1",
        "SHA1Cng",
        "SHA1CryptoServiceProvider",
        "SHA1Managed",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_langauge(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="member_access_expression"
                ),
            ):
                match = g.match_ast(shard.graph, member, "__0__")
                if (
                    shard.graph.nodes[match["__0__"]].get("label_text")
                    in insecure_cyphers
                ):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F052
QUERIES: graph_model.Queries = ((FINDING, csharp_insecure_hash),)
