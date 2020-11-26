# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from parse_java.assertions.inspect import (
    inspect,
)
from parse_java.parse import (
    parse_from_content,
)
from utils import (
    graph as g,
)
from utils.fs import (
    get_file_raw_content,
)
from utils.model import (
    Grammar,
)


@run_decorator
async def test_assertions() -> None:
    path = 'test/data/lib_path/f063_path_traversal/Test.java'
    graph = await parse_from_content(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    paths = g.flows(graph, sink_type='F063_PATH_TRAVERSAL')

    assert inspect(graph, paths[0]) == {
        "vars": {
            "request": {
                "type": "HttpServletRequest",
            },
            "response": {
                "type": "HttpServletResponse",
            },
        },
    }
