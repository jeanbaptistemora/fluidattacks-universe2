# Standard library
import json

# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from parse_antlr import (
    format_model,
    model_to_graph,
    parse,
)
from utils.fs import (
    get_file_raw_content,
)
from utils.graph import (
    export_graph,
    export_graph_as_json,
    graphviz_to_svg,
)
from utils.model import (
    Grammar,
)


@run_decorator
async def test_parse_csharp_success() -> None:
    path = 'test/data/lib_path/f073/Test.cs'
    data = await parse(
        Grammar.CSHARP,
        content=await get_file_raw_content(path),
        path=path,
    )

    assert 'Compilation_unit' in data
    data = data['Compilation_unit'][0]

    assert 'Namespace_member_declarations' in data
    data = data['Namespace_member_declarations'][0]

    assert 'Namespace_member_declaration' in data
    data = data['Namespace_member_declaration'][0]

    assert 'Type_declaration' in data
    data = data['Type_declaration'][0]

    assert 'Class_definition' in data
    data = data['Class_definition'][0]

    assert data == {
        "c": 0,
        "l": 1,
        "text": "class",
        "type": "CLASS",
    }


@run_decorator
async def test_parse_java9_success() -> None:
    path = 'test/data/lib_path/f031_cwe378/Test.java'
    data = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    assert 'CompilationUnit' in data
    data = data['CompilationUnit'][0]

    assert 'OrdinaryCompilation' in data
    data = data['OrdinaryCompilation'][0]

    assert 'ImportDeclaration' in data
    data = data['ImportDeclaration'][0]

    assert 'SingleTypeImportDeclaration' in data
    data = data['SingleTypeImportDeclaration'][0]

    assert data == {
        'c': 0,
        'l': 1,
        'text':
        'import',
        'type': 'IMPORT',
    }


@run_decorator
async def test_parse_scala_success() -> None:
    path = 'test/data/lib_path/f073/Test.scala'
    data = await parse(
        Grammar.SCALA,
        content=await get_file_raw_content(path),
        path=path,
    )

    assert 'CompilationUnit' in data
    data = data['CompilationUnit'][0]

    assert 'TopStatSeq' in data
    data = data['TopStatSeq'][0]

    assert 'TopStat' in data
    data = data['TopStat'][0]

    assert 'TmplDef' in data
    data = data['TmplDef'][0]

    assert data == {
        'c': 0,
        'l': 1,
        'text': 'object',
        'type': None,
    }


@run_decorator
async def test_parse_fail() -> None:
    path = 'test/data/lib_path/f011/yarn.lock'
    for grammar in Grammar:
        data = await parse(
            grammar,
            content=await get_file_raw_content(path),
            path=path,
        )

        assert data == {}


@run_decorator
async def test_graph_generation_easy() -> None:
    path = 'test/data/lib_path/f031_cwe378/Test.java'
    model = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )
    model = format_model(model)
    graph = model_to_graph(model)
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json.dumps(graph_as_json, indent=2, sort_keys=True)

    assert export_graph(graph, 'test/outputs/test_graph_generation_easy.graph')
    assert await graphviz_to_svg('test/outputs/test_graph_generation_easy.graph')

    with open('test/data/parse_antlr/graph_generation_easy.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected


@run_decorator
async def test_graph_generation_hard() -> None:
    path = 'test/data/benchmark/owasp/BenchmarkTest00008.java'
    model = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )
    model = format_model(model)
    graph = model_to_graph(model)
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json.dumps(graph_as_json, indent=2)

    assert export_graph(graph, 'test/outputs/test_graph_generation_hard.graph')
    assert await graphviz_to_svg('test/outputs/test_graph_generation_hard.graph')

    with open('test/data/parse_antlr/graph_generation_hard.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected
