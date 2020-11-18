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
from parse_antlr.parse import (
    parse,
)
from utils.graph import (
    has_label,
    export_graph,
    graphviz_to_svg,
)
from parse_java.parse import (
    from_antlr_model,
)


@run_decorator
async def test_apply_cfg() -> None:
    path = 'test/data/benchmark/owasp/BenchmarkTest00167.java'
    model = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    graph = from_antlr_model(model)

    export_graph(graph, 'test/outputs/test_apply_cfg.graph')
    await graphviz_to_svg('test/outputs/test_apply_cfg.graph')

    assert has_label(
        graph['795']['914'],
        'CFG',
        'True'
    )
    assert has_label(
        graph['1273']['1339'],
        'CFG',
        'True'
    )
    assert has_label(
        graph['2525']['2591'],
        'CFG',
        'True'
    )
    assert has_label(
        graph['3295']['3337'],
        'CFG',
        'True'
    )
    assert has_label(
        graph['3295']['3459'],
        'CFG',
        'False'
    )
