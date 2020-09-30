# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from parse_antlr import (
    parse,
)
from utils.fs import (
    get_file_raw_content,
)


@run_decorator
async def test_parse_csharp_success() -> None:
    path = 'test/data/lib_path/f073/Test.cs'
    data = await parse(
        'CSharp',
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
        'Java9',
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
async def test_parse_fail() -> None:
    path = 'test/data/lib_path/f011/yarn.lock'
    for grammar in ('CSharp', 'Java9'):
        data = await parse(
            grammar,  # type: ignore
            content=await get_file_raw_content(path),
            path=path,
        )

        assert data == {}
