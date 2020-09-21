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
    Block,
)


def test_bad() -> None:
    expected = 'ERROR'

    with open('test/data/parse_hcl2/bad.tf') as file:
        template = load(file.read(), default=expected)

    assert template == expected


def test_load_empty() -> None:
    expected = Tree('start', [
        Tree('body', [

        ])
    ])

    with open('test/data/parse_hcl2/empty.tf') as file:
        template = load(file.read())

    assert template == expected


def test_load_1() -> None:
    expected = Tree('start', [
        Tree('body', [
            Block(
                namespace=[
                    'module',
                    'iam_user',
                ],
                body=[
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
                        val={
                            'proyecto': '${var.proyecto}',
                            'analista': '${var.analista}',
                        },
                    ),
                ],
            ),
        ])
    ])

    with open('test/data/parse_hcl2/1.tf') as file:
        template = load(file.read())

    assert template == expected


def test_load_2() -> None:
    expected = Tree('start', [
        Tree('body', [
            Block(
                namespace=['resource', 'aws_sqs_queue', 'app_queue'],
                body=[
                    Attribute(key='name', val=Tree('get_attr_expr_term', [
                        Tree('identifier', ['var']),
                        Tree('identifier', ['queue_name'])
                    ])),
                    Attribute(key='tags', val=Tree('get_attr_expr_term', [
                        Tree('identifier', ['var']),
                        Tree('identifier', ['tags']),
                    ])),
                    Attribute(key='kms_master_key_id', val=Tree('get_attr_expr_term', [
                        Tree('identifier', ['var']),
                        Tree('identifier', ['keysqs_name']),
                    ])),
                    Attribute(key='kms_data_key_reuse_period_seconds', val=86400),
                ]),
            ]),
        ])

    with open('test/data/parse_hcl2/2.tf') as file:
        template = load(file.read())

    assert template == expected
