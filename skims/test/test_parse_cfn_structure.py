from metaloaders.cloudformation import (
    load,
)
from metaloaders.model import (
    Type,
)
from parse_cfn.structure import (
    iterate_iam_policy_documents,
)
import pytest

EXPECTED = (
    {
        "Effect": "Allow",
        "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
        "Resource": [{"Fn::Sub": "arn:aws:s3:::${pS3RestoreBucket}"}],
    },
    {
        "Effect": "Allow",
        "Action": [
            "s3:GetObjectMetaData",
            "s3:GetObject",
            "s3:PutObject",
            "s3:ListMultipartUploadParts",
            "s3:AbortMultipartUpload",
        ],
        "Resource": ["*"],
    },
    {
        "Action": [
            "logs:CreateLogStream",
            "logs:CreateLogGroup",
            "logs:PutLogEvents",
        ],
        "Effect": "Allow",
        "Resource": ["arn:aws:logs:*:*:*"],
    },
    {
        "Action": ["comprehend:Detect*", "comprehend:BatchDetect*"],
        "Effect": "Allow",
        "Resource": ["*"],
    },
    {
        "Effect": "Allow",
        "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
        "Resource": ["*"],
    },
    {
        "Effect": "Deny",
        "Condition": {"StringNotEquals": {"aws:RequestedRegion": "us-east-1"}},
        "Action": ["*"],
        "Resource": ["*"],
    },
    {
        "Effect": "Allow",
        "Action": ["sts:AssumeRole"],
        "Resource": ["arn:aws:iam::*:role/cloud-lambda"],
    },
)


@pytest.mark.skims_test_group("unittesting")
def test_iterate_iam_policy_documents_as_yml() -> None:
    with open("skims/test/data/parse_cfn/full.yaml", encoding="utf-8") as file:
        template = load(stream=file.read(), fmt="yaml")
    result = tuple(iterate_iam_policy_documents(template))

    assert tuple(item.raw for item in result) == EXPECTED

    assert len(result) == 7

    assert result[0].start_line == 18
    assert result[0].start_column == 12
    assert result[1].start_line == 24
    assert result[1].start_column == 12
    assert result[2].start_line == 39
    assert result[2].start_column == 16
    assert result[3].start_line == 49
    assert result[3].start_column == 16
    assert result[4].start_line == 62
    assert result[4].start_column == 12
    assert result[5].start_line == 75
    assert result[5].start_column == 16
    assert result[6].start_line == 84
    assert result[6].start_column == 14

    assert result[0].inner["Effect"].inner == "Allow"
    assert result[0].inner["Effect"].start_line == 18
    assert result[0].inner["Effect"].start_column == 20
    assert result[0].inner["Effect"].data_type == Type.STRING

    assert result[0].inner["Action"].start_line == 20
    assert result[0].inner["Action"].start_column == 14
    assert result[0].inner["Action"].data_type == Type.ARRAY
    assert result[0].inner["Action"].inner[0] == "s3:ListBucket"

    assert result[0].inner["Resource"].start_line == 23
    assert result[0].inner["Resource"].start_column == 14
    assert result[0].inner["Resource"].data_type == Type.ARRAY

    assert result[0].inner["Action"].data[1].inner == "s3:GetBucketLocation"
    assert result[0].inner["Action"].data[1].start_line == 21

    assert result[3].inner["Action"].start_line == 50
    assert result[3].inner["Action"].data_type == Type.ARRAY
    assert result[3].inner["Resource"].inner[0] == "*"
    assert result[3].inner["Resource"].start_line == 53
    assert result[3].inner["Resource"].start_column == 26

    assert result[6].start_line == 84
    assert result[6].data_type == Type.OBJECT
    assert result[6].inner["Effect"].data == "Allow"
    assert result[6].inner["Effect"].start_line == 84
    assert result[6].inner["Effect"].start_column == 22

    assert result[6].inner["Action"].data_type == Type.ARRAY
    assert result[6].inner["Action"].inner[0] == "sts:AssumeRole"
    assert result[6].inner["Resource"][0][0].start_line == 86


@pytest.mark.skims_test_group("unittesting")
def test_iterate_iam_policy_documents_as_json() -> None:
    with open(
        "skims/test/data/parse_cfn/full.yaml.json", encoding="utf-8"
    ) as file:
        template = load(stream=file.read(), fmt="json")

    result = tuple(iterate_iam_policy_documents(template))

    assert tuple(item.raw for item in result) == EXPECTED

    assert len(result) == 7

    assert result[0].start_line == 17
    assert result[0].start_column == 12
    assert result[1].start_line == 27
    assert result[1].start_column == 12
    assert result[2].start_line == 49
    assert result[2].start_column == 16
    assert result[3].start_line == 67
    assert result[3].start_column == 16
    assert result[4].start_line == 88
    assert result[4].start_column == 12
    assert result[5].start_line == 108
    assert result[5].start_column == 16
    assert result[6].start_line == 124
    assert result[6].start_column == 27

    assert result[0].inner["Effect"].inner == "Allow"
    assert result[0].inner["Effect"].start_line == 18
    assert result[0].inner["Effect"].start_column == 24
    assert result[0].inner["Effect"].data_type == Type.STRING

    assert result[0].inner["Action"].start_line == 19
    assert result[0].inner["Action"].start_column == 24
    assert result[0].inner["Action"].data_type == Type.ARRAY
    assert result[0].inner["Action"].inner[0] == "s3:ListBucket"

    assert result[0].inner["Resource"].start_line == 23
    assert result[0].inner["Resource"].start_column == 26
    assert result[0].inner["Resource"].data_type == Type.ARRAY

    assert result[0].inner["Action"].data[1].inner == "s3:GetBucketLocation"
    assert result[0].inner["Action"].data[1].start_line == 21

    assert result[3].inner["Action"].start_line == 68
    assert result[3].inner["Action"].data_type == Type.ARRAY
    assert result[3].inner["Resource"].inner[0] == "*"
    assert result[3].inner["Resource"].start_line == 73
    assert result[3].inner["Resource"].start_column == 30

    assert result[6].data_type == Type.OBJECT
    assert result[6].inner["Effect"].data == "Allow"
    assert result[6].inner["Effect"].start_line == 125
    assert result[6].inner["Effect"].start_column == 26

    assert result[6].inner["Action"].data_type == Type.ARRAY
    assert result[6].inner["Action"].inner[0] == "sts:AssumeRole"
    assert result[6].inner["Resource"][0][0].start_line == 127
