from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from symbolic_eval.types import (
    Analyzer,
)
from typing import (
    Dict,
)
from utils import (
    ctx,
)

ANALYZERS: Dict[FindingEnum, Analyzer] = {}


def analyze(language: GraphLanguage, graph: Graph) -> None:
    for finding in ctx.CTX.config.checks:
        if analyzer := ANALYZERS.get(finding):
            analyzer(language, graph)
