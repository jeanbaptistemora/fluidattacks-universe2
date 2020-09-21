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
                        column=2,
                        key='source',
                        line=4,
                        val='modules\\/iam-user',
                    ),
                    Attribute(
                        column=2,
                        key='name',
                        line=6,
                        val='${var.iamuser}',
                    ),
                    Attribute(
                        column=2,
                        key='force_destroy',
                        line=7,
                        val=True,
                    ),
                    Attribute(
                        column=2,
                        key='tags',
                        line=9,
                        val={
                            'proyecto': '${var.proyecto}',
                            'analista': '${var.analista}',
                        },
                    ),
                ],
                column=0,
                line=3,
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
                    Attribute(
                        column=2,
                        key='name',
                        line=2,
                        val=Tree('get_attr_expr_term', [
                            Tree('identifier', ['var']),
                            Tree('identifier', ['queue_name'])
                        ]),
                    ),
                    Attribute(
                        column=2,
                        key='tags',
                        line=3,
                        val=Tree('get_attr_expr_term', [
                            Tree('identifier', ['var']),
                            Tree('identifier', ['tags']),
                        ]),
                    ),
                    Attribute(
                        column=2,
                        key='kms_master_key_id',
                        line=4,
                        val=Tree('get_attr_expr_term', [
                            Tree('identifier', ['var']),
                            Tree('identifier', ['keysqs_name']),
                        ]),
                    ),
                    Attribute(
                        column=2,
                        key='kms_data_key_reuse_period_seconds',
                        line=5,
                        val=86400,
                    ),
                ],
                column=0,
                line=1,
            ),
            Block(
                namespace=['resource', 'aws_sns_topic_subscription', 'test'],
                body=[
                    Attribute(
                        column=2,
                        key='topic_arn',
                        line=9,
                        val='${aws_sns_topic.app_topic.arn}',
                    ),
                    Attribute(column=2, key='protocol', line=10, val='sqs'),
                    Attribute(
                        column=2,
                        key='endpoint',
                        line=11,
                        val='arn:aws:sqs:${var.zone}:${var.aws_account}:xxxx-${var.environment_prefix}',
                    ),
                    Attribute(
                        column=2,
                        key='filter_policy',
                        line=12,
                        val='{ "scope": [ "SEND_TO_UI", "SEND_TO_ALL" ] }',
                    ),
                    Attribute(
                        column=2,
                        key='raw_message_delivery',
                        line=13,
                        val=True,
                    ),
                ],
                column=0,
                line=8,
            ),
            Block(
                namespace=['resource', 'aws_iam_user_policy', 'topics_policy1'],
                body=[
                    Attribute(
                        column=2,
                        key='name',
                        line=17,
                        val='sns_policy',
                    ),
                    Attribute(
                        column=2,
                        key='user',
                        line=18,
                        val=Tree('get_attr_expr_term', [
                            Tree('identifier', ['var']),
                            Tree('identifier', ['arn_user']),
                        ]),
                    ),
                    Attribute(
                        column=2,
                        key='policy',
                        line=20,
                        val=Tree('heredoc_template', [
                            Token('__ANON_10', '<<EOF\n{\n    "Version": "2012-10-17",\n    "Statement": [\n        {\n            "Sid": "rule1",\n            "Effect": "Allow",\n            "Action": [\n                "sns:ListSubscriptionsByTopic",\n                "sns:Publish"\n            ],\n            "Resource": [\n                "${aws_sns_topic.test.arn}",\n                "${aws_sns_topic.test2.arn}"\n            ]\n        },\n        {\n            "Sid": "rule2",\n            "Effect": "Allow",\n            "Action": "sns:ListTopics",\n            "Resource": "*"\n        }\n    ]\n}\nEOF'),
                        ]),
                    ),
                ],
                column=0,
                line=16,
            ),
        ]),
    ])

    with open('test/data/parse_hcl2/2.tf') as file:
        template = load(file.read())

    assert template == expected
