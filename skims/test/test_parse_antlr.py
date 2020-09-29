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
async def test_parse_success() -> None:
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
    data = await parse(
        'Java9',
        content=await get_file_raw_content(path),
        path=path,
    )

    assert data == {}
