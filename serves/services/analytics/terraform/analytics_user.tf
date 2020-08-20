data "aws_iam_policy_document" "analytics_policy_document_data" {

  statement {
    sid = "AnalyticsS3"
    effect = "Allow"
    actions = [
      "s3:*",
    ]
    resources = [
      "arn:aws:s3:::fluidanalytics/*"
    ]
  }

  statement {
    sid = "AnalyticsReadDynamoDB"
    effect = "Allow"
    actions = [
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:Describe*",
      "dynamodb:List*",
      "dynamodb:BatchGetItem",
    ]
    resources = [
      "*"
    ]
  }

  statement {
    sid = "AnalyticsReadInfrastructure"
    effect = "Allow"
    actions = [
      "redshift:Describe*",
      "redshift:ViewQueriesInConsole",
      "sns:Get*",
      "sns:List*",
      "ec2:Describe*",
      "cloudwatch:Describe*",
      "cloudwatch:List*",
      "cloudwatch:Get*"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "analytics_policy" {
  name        = "analytics-policy"
  path        = "/analytics/"
  description = "Policy to allow Analytics to see the required AWS Resources"

  policy = data.aws_iam_policy_document.analytics_policy_document_data.json
}

resource "aws_iam_user" "analytics_user" {
  name     = "analytics"
  path     = "/analytics/"
}

resource "aws_iam_user_policy_attachment" "attach_analytics_policy" {
  policy_arn = aws_iam_policy.analytics_policy.arn
  user       = aws_iam_user.analytics_user.name
}
