# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from parse_antlr import (
    parse,
    format_model,
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
    model = format_model(await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    ))

    assert len(tuple(yield_normal_class(model))) == 1
    assert len(tuple(yield_normal_class_methods(model))) == 2
