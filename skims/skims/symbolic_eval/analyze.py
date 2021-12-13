from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from symbolic_eval.f008.analyze import (
    analyze as analyze_f008,
)
from symbolic_eval.f100.analyze import (
    analyze as analyze_f100,
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

ANALYZERS: Dict[FindingEnum, Analyzer] = {
    FindingEnum.F008: analyze_f008,
    FindingEnum.F100: analyze_f100,
}


def analyze(language: GraphLanguage, graph: Graph) -> None:
    for finding in ctx.CTX.config.checks:
        if analyzer := ANALYZERS.get(finding):
            analyzer(language, graph)
