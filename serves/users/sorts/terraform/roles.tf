# sorts_sagemaker role definition
data "aws_iam_policy_document" "sorts_sagemaker_assume_policy" {
  statement {
    sid    = "SageMakerAssumeRolePolicy"
    effect = "Allow"

    principals {
      type = "Service"
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
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::sorts",
      "arn:aws:s3:::sorts/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:ListAllMyBuckets",
      "s3:GetBucketLocation"
    ]
    resources = [
      "arn:aws:s3:::*"
    ]
  }

  statement {
    actions = [
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::sorts"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject"
    ]
    resources = [
      "arn:aws:s3:::sorts/sorts-training*/*",
      "arn:aws:s3:::sorts/training-output/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "cloudwatch:PutMetricData"
    ]
    resources = [
      "*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:CreateLogGroup",
      "logs:DescribeLogStreams"
    ]
    resources = [
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/sagemaker/TrainingJobs",
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/sagemaker/TrainingJobs:log-stream:*"
    ]
  }
}

resource "aws_iam_role" "sorts_sagemaker" {
  name               = "sorts_sagemaker"
  assume_role_policy = data.aws_iam_policy_document.sorts_sagemaker_assume_policy.json

  tags = {
    "Name"               = "sorts_sagemaker"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_role_policy" "sorts_sagemaker_policy" {
  name   = "sorts_sagemaker_policy"
  policy = data.aws_iam_policy_document.sorts_sagemaker_policy.json
  role   = aws_iam_role.sorts_sagemaker.id
}

# sorts-prod role definition
data "aws_iam_policy_document" "sorts_prod_assume_policy" {
  statement {
    sid    = "OktaSAMLAccess"
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithSAML"
    ]
    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:saml-provider/okta-saml-provider"]
    }
    condition {
      test     = "StringEquals"
      variable = "SAML:aud"

      values = [
        "https://signin.aws.amazon.com/saml"
      ]
    }
  }
}

resource "aws_iam_role" "sorts-prod" {
  name               = "sorts-prod"
  assume_role_policy = data.aws_iam_policy_document.sorts_prod_assume_policy.json

  tags = {
    "Name"               = "sorts-prod"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_role_policy" "sorts-prod_policy" {
  name   = "sorts-prod_policy"
  policy = data.aws_iam_policy_document.sorts_sagemaker_policy.json
  role   = aws_iam_role.sorts_sagemaker.id
}
