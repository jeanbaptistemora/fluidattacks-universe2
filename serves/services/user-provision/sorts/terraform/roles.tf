data "aws_iam_policy_document" "sorts_sagemaker_assume_policy" {
  statement {
    sid    = "SageMakerAssumeRolePolicy"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = [
        "sagemaker.amazonaws.com"
      ]
    }

    actions = [
      "sts:AssumeRole",
    ]
  }
}

data "aws_iam_policy_document" "sorts_sagemaker_policy" {
  statement {
    effect = "Allow"
    actions = [
      "s3:Get*",
      "s3:List*"
    ]
    resources = [
      "arn:aws:s3:::sorts",
      "arn:aws:s3:::sorts/training",
      "arn:aws:s3:::sorts/training/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject"
    ]
    resources = [
      "arn:aws:s3:::sorts/sorts_training*/*"
    ]
  }
}

resource "aws_iam_role" "sorts_sagemaker" {
  name = "sorts_sagemaker"
  assume_role_policy = data.aws_iam_policy_document.sorts_sagemaker_assume_policy.json

  tags = {
    "Name"               = "sorts_sagemaker"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_role_policy" "sorts_sagemaker_policy" {
  name = "sorts_sagemaker_policy"
  policy = data.aws_iam_policy_document.sorts_sagemaker_policy.json
  role = aws_iam_role.sorts_sagemaker.id
}
