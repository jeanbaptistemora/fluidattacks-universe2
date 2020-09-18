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
                        val=Tree('expr_term', [
                            'modules\\/iam-user'
                        ]),
                    ),
                    Attribute(
                        key='name',
                        val=Tree('expr_term', [
                            '${var.iamuser}'
                        ]),
                    ),
                    Attribute(
                        key='force_destroy',
                        val=Tree('expr_term', [
                            True,
                        ]),
                    ),
                    Attribute(
                        key='tags',
                        val=Tree('expr_term', [
                            Tree('object', [
                                Tree('object_elem', [
                                    Tree('identifier', [
                                        'proyecto'
                                    ]),
                                    Tree('expr_term', [
                                        '${var.proyecto}'
                                    ])
                                ]),
                                Tree('object_elem', [
                                    Tree('identifier', [
                                        'analista'
                                    ]),
                                    Tree('expr_term', [
                                        '${var.analista}'
                                    ])
                                ]),
                            ])
                        ]),
                    ),
                ]),
            ])
        ])
    ])

    with open('test/data/parse_hcl2/full.tf') as file:
        template = load(file.read())

    assert template == expected
