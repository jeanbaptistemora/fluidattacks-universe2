# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from parse_antlr.parse import (
    parse,
)
from parse_antlr.model import (
    from_parse_tree as model_from_parse_tree,
)
from parse_java.structure import (
    yield_normal_class,
    yield_normal_class_methods,
)
from utils.fs import (
    get_file_raw_content,
)
from utils.model import (
    Grammar,
)


@run_decorator
async def test_structure() -> None:
    path = 'test/data/benchmark/owasp/BenchmarkTest00008.java'
    parse_tree = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )
    model = model_from_parse_tree(parse_tree)

    assert len(tuple(yield_normal_class(model))) == 1
    assert len(tuple(yield_normal_class_methods(model))) == 2
