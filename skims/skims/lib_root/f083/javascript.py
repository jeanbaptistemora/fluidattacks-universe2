from collections.abc import (
    Iterator,
)
from lib_root.f083.common import (
    get_vuln_nodes,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def js_xml_parser(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_XML_PARSER

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            for n_id in get_vuln_nodes(shard.syntax_graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f083.generic_xml_parser",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
