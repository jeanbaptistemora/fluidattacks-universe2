from __future__ import (
    annotations,
)

from model import (
    graph_model,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
    Set,
    Tuple,
)
from utils.logs import (
    log_blocking,
)


class SyntaxReaderArgs(NamedTuple):
    generic: Callable[[Any], graph_model.SyntaxSteps]
    graph: graph_model.Graph
    language: graph_model.GraphShardMetadataLanguage
    n_id: graph_model.NId

    def fork_n_id(self, n_id: graph_model.NId) -> SyntaxReaderArgs:
        return SyntaxReaderArgs(
            generic=self.generic,
            graph=self.graph,
            language=self.language,
            n_id=n_id,
        )


SyntaxReader = Callable[[SyntaxReaderArgs], graph_model.SyntaxStepsLazy]
SyntaxReaders = Tuple[SyntaxReader, ...]


class Dispatcher(NamedTuple):
    applicable_languages: Set[graph_model.GraphShardMetadataLanguage]
    applicable_node_label_types: Set[str]
    syntax_reader: SyntaxReader


Dispatchers = Tuple[Dispatcher, ...]


class MissingSyntaxReader(Exception):
    pass


class MissingCaseHandling(Exception):
    def __init__(self, reader_args: SyntaxReaderArgs) -> None:
        log_blocking("debug", "Missing case handling: %s", reader_args.n_id)
        super().__init__()
