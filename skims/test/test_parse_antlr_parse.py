# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from model import (
    core_model,
)
from parse_antlr.parse import (
    parse,
)
from utils.fs import (
    get_file_raw_content,
)


@run_decorator
@pytest.mark.skims_test_group('unittesting')
async def test_parse_csharp_success() -> None:
    path = 'skims/test/data/lib_path/f073/Test.cs'
    data = await parse(
        core_model.Grammar.CSHARP,
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
@pytest.mark.skims_test_group('unittesting')
async def test_parse_java9_success() -> None:
    path = 'skims/test/data/lib_path/f031_cwe378/Test.java'
    data = await parse(
        core_model.Grammar.JAVA9,
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
@pytest.mark.skims_test_group('unittesting')
async def test_parse_scala_success() -> None:
    path = 'skims/test/data/lib_path/f073/Test.scala'
    data = await parse(
        core_model.Grammar.SCALA,
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
@pytest.mark.skims_test_group('unittesting')
async def test_parse_fail() -> None:
    path = 'skims/test/data/lib_path/f011/yarn.lock'
    for grammar in core_model.Grammar:
        data = await parse(
            grammar,
            content=await get_file_raw_content(path),
            path=path,
        )

        assert data == {}
