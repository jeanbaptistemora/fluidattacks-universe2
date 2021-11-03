from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from typing import (
    Callable,
)

Analyzer = Callable[[GraphLanguage, Graph], None]
LanguageAnalyzer = Callable[[Graph], None]
