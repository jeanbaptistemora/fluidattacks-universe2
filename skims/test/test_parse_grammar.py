# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from parse_grammar import (
    parse,
)


@run_decorator
async def test_parse_success() -> None:
    data = await parse('Java9', 'test/data/lib_path/f031_cwe378/Test.java')

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
    data = await parse('Java9', 'test/data/lib_path/f011/yarn.lock')

    assert data == {}
