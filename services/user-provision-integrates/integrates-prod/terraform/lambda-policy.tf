data "aws_iam_policy_document" "integrates-prod-lambda-policy-data" {
  statement {
    effect  = "Allow"
    actions = ["lambda:*"]
    resources = [
      "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:fi_binaryalert*",
      "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:integrates-*"
    ]
  }
  statement {
    effect  = "Allow"
    actions = ["logs:*"]
    resources = [
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/integrates-*",
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/fi_binaryalert*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "lambda:UpdateEventSourceMapping",
      "lambda:ListEventSourceMappings",
      "lambda:GetEventSourceMapping",
      "lambda:DeleteEventSourceMapping",
      "lambda:CreateEventSourceMapping"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "integrates-prod-lambda-policy" {
  description = "integrates-prod policy for lambda"
  name        = "${var.user-name}-lambda-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-lambda-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-lambda" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-lambda-policy.arn
}
