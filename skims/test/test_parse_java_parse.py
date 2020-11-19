# Standard library
import json

# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from parse_antlr.parse import (
    parse,
)
from parse_antlr.model import (
    from_parse_tree as model_from_parse_tree,
)
from parse_java.parse import (
    from_antlr_model,
    parse_from_content,
)
from parse_java.graph.control_flow import (
    analyze as analyze_control_flow,
)
from utils.fs import (
    get_file_raw_content,
)
from utils.graph import (
    export_graph,
    export_graph_as_json,
    graphviz_to_svg,
    has_label,
)
from utils.model import (
    Grammar,
)


@pytest.mark.parametrize(  # type: ignore
    'path,name',
    [
        (
            'test/data/lib_path/f031_cwe378/Test.java',
            'small_java_program',
        ),
        (
            'test/data/benchmark/owasp/BenchmarkTest00008.java',
            'owasp_benchmark_00008',
        ),
        (
            'test/data/benchmark/owasp/BenchmarkTest00167.java',
            'owasp_benchmark_00167'
        )
    ],
)
@run_decorator
async def test_graph_generation(path: str, name: str) -> None:
    content = await get_file_raw_content(path)

    # Old way
    parse_tree = await parse(Grammar.JAVA9, content=content, path=path)
    model = model_from_parse_tree(parse_tree)
    model_as_json = json.dumps(model, indent=2)
    graph = from_antlr_model(model)

    # New way, comprised
    graph = await parse_from_content(Grammar.JAVA9, content=content, path=path)
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json.dumps(graph_as_json, indent=2, sort_keys=True)

    assert export_graph(graph, f'test/outputs/{name}.graph')
    assert await graphviz_to_svg(f'test/outputs/{name}.graph')

    with open(f'test/outputs/{name}.model.json', 'w') as handle:
        handle.write(model_as_json)

    with open(f'test/data/parse_java/{name}.graph.json', 'w') as handle:
        handle.write(graph_as_json_str)

    with open(f'test/data/parse_java/{name}.graph.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected


@run_decorator
async def test_apply_control_flow() -> None:
    path = 'test/data/parse_java/TestCFG.java'
    parse_tree = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )
    model = model_from_parse_tree(parse_tree)
    graph = from_antlr_model(model)

    export_graph(graph, 'test/outputs/test_apply_control_flow.graph')
    await graphviz_to_svg('test/outputs/test_apply_control_flow.graph')

    # Check IfThenStatement and IfThenElseStatement
    assert has_label(graph['352']['396'], label_cfg='CFG', label_true='True')
    assert has_label(graph['460']['483'], label_cfg='CFG', label_true='True')
    assert has_label(graph['531']['554'], label_cfg='CFG', label_true='True')
    assert has_label(graph['531']['601'], label_cfg='CFG', label_false='False')
    assert has_label(graph['649']['729'], label_cfg='CFG', label_false='False')
    assert has_label(graph['649']['682'], label_cfg='CFG', label_true='True')
    assert has_label(graph['730']['763'], label_cfg='CFG', label_true='True')
    assert has_label(graph['730']['810'], label_cfg='CFG', label_false='False')
    assert has_label(graph['2623']['2659'], label_cfg='CFG', label_true='True')
    assert has_label(graph['2843']['2879'], label_cfg='CFG', label_true='True')
    assert has_label(graph['3333']['3402'], label_cfg='CFG', label_true='True')

    # Check BlockStatement
    assert has_label(graph['98']['132'], label_cfg='CFG', label_e='e')
    assert has_label(graph['132']['169'], label_cfg='CFG', label_e='e')
    assert has_label(graph['169']['459'], label_cfg='CFG', label_e='e')
    assert has_label(graph['459']['530'], label_cfg='CFG', label_e='e')
    assert has_label(graph['530']['648'], label_cfg='CFG', label_e='e')
    assert has_label(graph['893']['908'], label_cfg='CFG', label_e='e')
    assert has_label(graph['908']['1213'], label_cfg='CFG', label_e='e')
