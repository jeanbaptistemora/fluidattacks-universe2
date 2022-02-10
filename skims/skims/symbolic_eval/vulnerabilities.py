from ctx import (
    CTX,
)
from model.core_model import (
    MethodsEnum,
    Vulnerability,
)
from model.graph_model import (
    GRAPH_VULNERABILITY_PARAMETERS,
    GraphShard,
    NId,
)
import os
from utils import (
    fs,
    string,
)
from vulnerabilities import (
    build_lines_vuln,
    build_metadata,
)
from zone import (
    t,
)


def create_vulnerability(
    shard: GraphShard,
    n_id: NId,
    method: MethodsEnum,
) -> Vulnerability:
    node_attrs = shard.graph.nodes[n_id]
    line = node_attrs["label_l"]
    column = node_attrs["label_c"]

    params = GRAPH_VULNERABILITY_PARAMETERS[method.value.finding]
    desc_key = params.desc_key
    desc_params = params.desc_params

    full_path = os.path.join(CTX.config.working_dir, shard.path)

    return build_lines_vuln(
        method=method,
        what=shard.path,
        where=str(line),
        metadata=build_metadata(
            method=method,
            description=(
                f"{t(key=desc_key, **desc_params)} {t(key='words.in')} "
                f"{CTX.config.namespace}/{shard.path}"
            ),
            snippet=string.make_snippet(
                content=fs.sync_get_file_content(full_path),
                viewport=string.SnippetViewport(
                    column=int(column),
                    line=int(line),
                ),
            ),
        ),
    )
