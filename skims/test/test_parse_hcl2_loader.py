from lark import (
    Tree,
)
from parse_hcl2.loader import (
    load_blocking,
)
from parse_hcl2.tokens import (
    Attribute,
    Block,
    Json,
)
import pytest


@pytest.mark.skims_test_group("unittesting")
def test_bad() -> None:
    expected = "ERROR"

    with open(
        "skims/test/data/parse_hcl2/bad.nottf", encoding="utf-8"
    ) as file:
        template = load_blocking(file.read(), default=expected)

    assert template == expected


@pytest.mark.skims_test_group("unittesting")
def test_load_empty() -> None:
    expected = Tree("start", [Tree("body", [])])

    with open("skims/test/data/parse_hcl2/empty.tf", encoding="utf-8") as file:
        template = load_blocking(file.read())

    assert template == expected


@pytest.mark.skims_test_group("unittesting")
def test_load_1() -> None:
    expected = Tree(
        "start",
        [
            Tree(
                "body",
                [
                    Block(
                        namespace=["module", "iam_user"],
                        body=[
                            Attribute(
                                column=2,
                                key="source",
                                line=4,
                                val="modules/iam-user",
                            ),
                            Attribute(
                                column=2,
                                key="name",
                                line=6,
                                val=Tree(
                                    "get_attr_expr_term",
                                    [
                                        Tree("identifier", ["var"]),
                                        Tree("identifier", ["iamuser"]),
                                    ],
                                ),
                            ),
                            Attribute(
                                column=2, key="force_destroy", line=7, val=True
                            ),
                            Attribute(
                                column=2,
                                key="tags",
                                line=9,
                                val={
                                    "proyecto": "${var.proyecto}",
                                    "analista": "${var.analista}",
                                },
                            ),
                        ],
                        column=0,
                        line=3,
                    )
                ],
            )
        ],
    )

    with open("skims/test/data/parse_hcl2/1.tf", encoding="utf-8") as file:
        template = load_blocking(file.read())

    assert template == expected


@pytest.mark.skims_test_group("unittesting")
def test_load_2() -> None:
    expected = Tree(
        "start",
        [
            Tree(
                "body",
                [
                    Block(
                        namespace=["resource", "aws_sqs_queue", "app_queue"],
                        body=[
                            Attribute(
                                column=2,
                                key="name",
                                line=2,
                                val=Tree(
                                    "get_attr_expr_term",
                                    [
                                        Tree("identifier", ["var"]),
                                        Tree("identifier", ["queue_name"]),
                                    ],
                                ),
                            ),
                            Attribute(
                                column=2,
                                key="tags",
                                line=3,
                                val=Tree(
                                    "get_attr_expr_term",
                                    [
                                        Tree("identifier", ["var"]),
                                        Tree("identifier", ["tags"]),
                                    ],
                                ),
                            ),
                            Attribute(
                                column=2,
                                key="kms_master_key_id",
                                line=4,
                                val=Tree(
                                    "get_attr_expr_term",
                                    [
                                        Tree("identifier", ["var"]),
                                        Tree("identifier", ["keysqs_name"]),
                                    ],
                                ),
                            ),
                            Attribute(
                                column=2,
                                key="kms_data_key_reuse_period_seconds",
                                line=5,
                                val=86400,
                            ),
                        ],
                        column=0,
                        line=1,
                    ),
                    Block(
                        namespace=[
                            "resource",
                            "aws_sns_topic_subscription",
                            "test",
                        ],
                        body=[
                            Attribute(
                                column=2,
                                key="topic_arn",
                                line=9,
                                val=Tree(
                                    "get_attr_expr_term",
                                    [
                                        Tree(
                                            "get_attr_expr_term",
                                            [
                                                Tree(
                                                    "identifier",
                                                    ["aws_sns_topic"],
                                                ),
                                                Tree(
                                                    "identifier", ["app_topic"]
                                                ),
                                            ],
                                        ),
                                        Tree("identifier", ["arn"]),
                                    ],
                                ),
                            ),
                            Attribute(
                                column=2, key="protocol", line=10, val="sqs"
                            ),
                            Attribute(
                                column=2,
                                key="endpoint",
                                line=11,
                                val="arn:aws:sqs:${var.zone}:"
                                "${var.aws_account}:"
                                "xxxx-${var.environment_prefix}",
                            ),
                            Attribute(
                                column=2,
                                key="filter_policy",
                                line=12,
                                val='{ \\"scope\\": [ \\"SEND_TO_UI\\", '
                                '\\"SEND_TO_ALL\\" ] }',
                            ),
                            Attribute(
                                column=2,
                                key="raw_message_delivery",
                                line=13,
                                val=True,
                            ),
                        ],
                        column=0,
                        line=8,
                    ),
                    Block(
                        namespace=[
                            "resource",
                            "aws_iam_user_policy",
                            "topics_policy1",
                        ],
                        body=[
                            Attribute(
                                column=2, key="name", line=17, val="sns_policy"
                            ),
                            Attribute(
                                column=2,
                                key="user",
                                line=18,
                                val=Tree(
                                    "get_attr_expr_term",
                                    [
                                        Tree("identifier", ["var"]),
                                        Tree("identifier", ["arn_user"]),
                                    ],
                                ),
                            ),
                            Attribute(
                                column=2,
                                key="policy",
                                line=20,
                                val=Json(
                                    column=11,
                                    data={
                                        "Version": "2012-10-17",
                                        "Statement": [
                                            {
                                                "Sid": "rule1",
                                                "Effect": "Allow",
                                                "Action": [
                                                    "sns:List"
                                                    + "SubscriptionsByTopic",
                                                    "sns:Publish",
                                                ],
                                                "Resource": [
                                                    "${aws_sns_topic."
                                                    "test.arn}",
                                                    "${aws_sns_topic."
                                                    "test2.arn}",
                                                ],
                                            },
                                            {
                                                "Sid": "rule2",
                                                "Effect": "Allow",
                                                "Action": "sns:ListTopics",
                                                "Resource": "*",
                                            },
                                        ],
                                    },
                                    line=20,
                                ),
                            ),
                        ],
                        column=0,
                        line=16,
                    ),
                ],
            )
        ],
    )

    with open("skims/test/data/parse_hcl2/2.tf", encoding="utf-8") as file:
        template = load_blocking(file.read())

    assert template == expected
