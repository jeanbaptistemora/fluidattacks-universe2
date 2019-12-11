data "aws_iam_policy_document" "integrates-prod-iam-policy-data" {
  statement {
    effect = "Allow"
    actions = [
      "iam:List*",
      "iam:Get*"
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["iam:*"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/integrates-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/fi_binaryalert*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/integrates-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/fi_binaryalert*"
    ]
  }
  statement {
    effect  = "Allow"
    actions = ["iam:PassRole"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable"
    ]
  }
}

resource "aws_iam_policy" "integrates-prod-iam-policy" {
  description = "integrates-prod policy for iam"
  name        = "${var.user-name}-iam-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-iam-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-iam" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-iam-policy.arn
}
