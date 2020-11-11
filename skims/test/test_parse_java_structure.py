# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from parse_antlr import (
    parse,
)
from parse_java.structure import (
    yield_normal_class_declaration,
)
from utils.fs import (
    get_file_raw_content,
)
from utils.model import (
    Grammar,
)


@run_decorator
async def test_yield_normal_class_declaration() -> None:
    path = 'test/data/benchmark/owasp/BenchmarkTest00008.java'
    model = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    assert len(tuple(yield_normal_class_declaration(model))) == 1
