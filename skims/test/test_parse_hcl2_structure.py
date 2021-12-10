from aws.model import (
    AWSIamPolicyStatement,
)
from parse_hcl2.common import (
    iterate_resources,
)
from parse_hcl2.loader import (
    load_blocking,
)
from parse_hcl2.structure.aws import (
    iterate_iam_policy_documents,
)
import pytest


@pytest.mark.skims_test_group("unittesting")
def test_iterate_resources() -> None:
    with open("skims/test/data/parse_hcl2/iam.tf", encoding="utf-8") as file:
        model = load_blocking(file.read())

    assert (
        len(tuple(iterate_resources(model, "resource", "aws_iam_role"))) == 1
    )


@pytest.mark.skims_test_group("unittesting")
def test_iterate_iam_policy_documents() -> None:
    with open("skims/test/data/parse_hcl2/iam.tf", encoding="utf-8") as file:
        model = load_blocking(file.read())

    assert tuple(iterate_iam_policy_documents(model)) == (
        AWSIamPolicyStatement(
            column=2,
            data={
                "Effect": "Allow",
                "Action": [
                    "s3:ListAllMyBuckets",
                    "s3:GetBucketLocation",
                ],
                "Sid": "1",
                "Resource": [
                    "arn:aws:s3:::*",
                ],
            },
            line=103,
        ),
        AWSIamPolicyStatement(
            column=2,
            data={
                "Effect": "Allow",
                "Action": ["s3:ListBucket"],
                "Resource": ["arn:aws:s3:::${var.s3_bucket_name}"],
                "Condition": "set",
            },
            line=116,
        ),
        AWSIamPolicyStatement(
            column=2,
            data={
                "Effect": "Deny",
                "Action": [
                    "s3:*",
                ],
                "Resource": [
                    "arn:aws:s3:::${var.s3_bucket_name}/home/&{aws:username}",
                    (
                        "arn:aws:s3:::${var.s3_bucket_name}"
                        "/home/&{aws:username}/*"
                    ),
                ],
            },
            line=137,
        ),
        AWSIamPolicyStatement(
            column=23,
            data={
                "Action": ["sts:AssumeRole"],
                "Principal": {
                    "Service": "ec2.amazonaws.com",
                },
                "Effect": "Allow",
            },
            line=5,
        ),
        AWSIamPolicyStatement(
            column=11,
            data={
                "Action": ["ec2:Describe*"],
                "Effect": "Allow",
                "Resource": ["*"],
            },
            line=45,
        ),
        AWSIamPolicyStatement(
            column=11,
            data={
                "Action": ["ec2:Describe*"],
                "Effect": "Allow",
                "Resource": ["*"],
            },
            line=66,
        ),
        AWSIamPolicyStatement(
            column=11,
            data={
                "Action": ["ec2:Describe*"],
                "Effect": "Allow",
                "Resource": ["*"],
            },
            line=25,
        ),
        AWSIamPolicyStatement(
            column=11,
            data={
                "Action": ["ec2:Describe*"],
                "Effect": "Allow",
                "Resource": ["*"],
            },
            line=86,
        ),
    )
