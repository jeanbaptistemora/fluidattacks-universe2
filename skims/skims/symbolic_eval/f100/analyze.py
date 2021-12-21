from model.core_model import (
    Vulnerabilities,
)
from model.graph_model import (
    GraphShard,
    GraphShardMetadataLanguage as GraphLanguage,
)
from symbolic_eval.f100.c_sharp import (
    analyze as c_sharp_analyzer,
)
from symbolic_eval.types import (
    LanguageAnalyzer,
    MissingLanguageAnalizer,
)
from typing import (
    Dict,
)
from utils import (
    logs,
)

LANGUAGE_ANALYZERS: Dict[GraphLanguage, LanguageAnalyzer] = {
    GraphLanguage.CSHARP: c_sharp_analyzer,
}


def get_lang_analyzer(language: GraphLanguage) -> LanguageAnalyzer:
    if lang_analyzer := LANGUAGE_ANALYZERS.get(language):
        return lang_analyzer
    raise MissingLanguageAnalizer(language.name)


def analyze(shard: GraphShard) -> Vulnerabilities:
    try:
        language = shard.metadata.language
        lang_analyzer = get_lang_analyzer(language)
        return tuple(lang_analyzer(shard))
    except MissingLanguageAnalizer:
        logs.log_blocking("error", "No analyzer for %s in F100", language.name)
        return tuple()
