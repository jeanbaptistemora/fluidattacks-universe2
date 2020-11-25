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
