from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphShard,
)
from symbolic_eval.f008.analyze import (
    analyze as analyze_f008,
)
from symbolic_eval.f100.analyze import (
    analyze as analyze_f100,
)
from symbolic_eval.types import (
    Analyzer,
    MissingAnalizer,
)
from typing import (
    Dict,
)
from utils import (
    logs,
)

ANALYZERS: Dict[FindingEnum, Analyzer] = {
    FindingEnum.F008: analyze_f008,
    FindingEnum.F100: analyze_f100,
}


def get_analyzer(finding: FindingEnum) -> Analyzer:
    if analyzer := ANALYZERS.get(finding):
        return analyzer
    raise MissingAnalizer(finding.name)


def analyze(shard: GraphShard, finding: FindingEnum) -> Vulnerabilities:
    try:
        analyzer = get_analyzer(finding)
        result = analyzer(shard)
        return result
    except MissingAnalizer:
        logs.log_blocking("error", "No symbolic analyzer for %s", finding.name)
        return tuple()
