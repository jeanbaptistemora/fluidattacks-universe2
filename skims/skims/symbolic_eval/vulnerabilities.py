from model.core_model import (
    FindingEnum,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from model.graph_model import (
    GRAPH_VULNERABILITY_PARAMETERS,
    GraphShard,
    NId,
)
import os
from utils import (
    ctx,
    fs,
    string,
)
from zone import (
    t,
)


def create_vulnerability(
    finding: FindingEnum, shard: GraphShard, n_id: NId, source_method: str
) -> Vulnerability:
    node_attrs = shard.graph.nodes[n_id]
    line = node_attrs["label_l"]
    column = node_attrs["label_c"]

    params = GRAPH_VULNERABILITY_PARAMETERS[finding]
    desc_key = params.desc_key
    desc_params = params.desc_params

    full_path = os.path.join(ctx.CTX.config.working_dir, shard.path)

    return Vulnerability(
        finding=finding,
        kind=VulnerabilityKindEnum.LINES,
        namespace=ctx.CTX.config.namespace,
        state=VulnerabilityStateEnum.OPEN,
        what=shard.path,
        where=str(line),
        skims_metadata=SkimsVulnerabilityMetadata(
            cwe=finding.value.cwe,
            description=(
                f"{t(key=desc_key, **desc_params)} {t(key='words.in')} "
                f"{ctx.CTX.config.namespace}/{shard.path}"
            ),
            snippet=string.make_snippet(
                content=fs.sync_get_file_content(full_path),
                viewport=string.SnippetViewport(
                    column=int(column),
                    line=int(line),
                ),
            ),
            source_method=source_method,
        ),
    )
