# Standard library
from __future__ import (
    annotations,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
    Set,
    Tuple,
)

# Local libraries
from model import (
    graph_model,
)
from utils.function import (
    get_id,
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
    syntax_readers: SyntaxReaders


Dispatchers = Tuple[Dispatcher, ...]


class MissingSyntaxReader(Exception):
    pass


class MissingCaseHandling(Exception):

    def __init__(
        self,
        reader: SyntaxReader,
        reader_args: SyntaxReaderArgs,
    ) -> None:
        log_blocking(
            'debug', 'Missing case handling: %s, %s',
            get_id(reader), reader_args.n_id,
        )
        super().__init__()
