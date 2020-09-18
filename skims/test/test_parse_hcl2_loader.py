# Third party libraries
from lark import (
    Tree,
)
from lark.lexer import (
    Token,
)

# Local libraries
from parse_hcl2.loader import (
    load,
)
from parse_hcl2.tokens import (
    Attribute,
)


def test_load_empty() -> None:
    expected = Tree('start', [
        Tree('body', [

        ])
    ])

    with open('test/data/parse_hcl2/empty.tf') as file:
        template = load(file.read())

    assert template == expected


def test_load_full() -> None:
    expected = Tree('start', [
        Tree('body', [
            Tree('block', [
                Tree('identifier', [
                    'module'
                ]),
                'iam_user',
                Tree('body', [
                    Attribute(
                        key='source',
                        val='modules\\/iam-user',
                    ),
                    Attribute(
                        key='name',
                        val='${var.iamuser}',
                    ),
                    Attribute(
                        key='force_destroy',
                        val=True,
                    ),
                    Attribute(
                        key='tags',
                        val=Tree('object', [
                            Tree('object_elem', [
                                Tree('identifier', [
                                    'proyecto'
                                ]),
                                '${var.proyecto}',
                            ]),
                            Tree('object_elem', [
                                Tree('identifier', [
                                    'analista'
                                ]),
                                '${var.analista}',
                            ]),
                        ]),
                    ),
                ]),
            ])
        ])
    ])

    with open('test/data/parse_hcl2/full.tf') as file:
        template = load(file.read())

    assert template == expected
