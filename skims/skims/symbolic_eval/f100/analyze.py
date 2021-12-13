from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from symbolic_eval.f100.c_sharp import (
    analyze as c_sharp_analyzer,
)
from symbolic_eval.types import (
    LanguageAnalyzer,
)
from typing import (
    Dict,
)

LANGUAGE_ANALYZERS: Dict[GraphLanguage, LanguageAnalyzer] = {
    GraphLanguage.CSHARP: c_sharp_analyzer,
}


def analyze(language: GraphLanguage, graph: Graph) -> None:
    if language_analyzer := LANGUAGE_ANALYZERS.get(language):
        language_analyzer(graph)
