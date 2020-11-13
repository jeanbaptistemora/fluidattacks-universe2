# Third party libraries
from aioextensions import (
    run_decorator,

)
from utils.fs import (
    get_file_raw_content,
)

# Local libraries
from utils.model import (
    Grammar,
)
from parse_antlr import (
    parse,
)
from parse_java_as_graph import from_model


@run_decorator
async def test_nodes() -> None:
    path = 'test/data/benchmark/owasp/BenchmarkTest00167.java'
    model = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    graph = from_model(model=model)

    assert graph.number_of_nodes() == 4294
    assert graph.number_of_edges() == 4293
    assert len(
        tuple(node for _, node in graph.nodes.data()
              if node.get('type', None) == 'CompilationUnit')) == 1
    random = tuple(node for _, node in graph.nodes.data()
                   if node.get('type', None) == 'Identifier'
                   and node.get('text', None) == 'Random')
    assert len(random) == 1
