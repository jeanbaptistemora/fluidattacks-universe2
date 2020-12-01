data "aws_iam_policy_document" "sorts_sagemaker" {
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
}

resource "aws_iam_role" "sorts_sagemaker" {
  name = "sorts_sagemaker"
  assume_role_policy = data.aws_iam_policy_document.sorts_sagemaker.json

  tags = {
    "Name"               = "sorts_sagemaker"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}
