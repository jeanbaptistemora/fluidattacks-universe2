data "aws_iam_policy_document" "integrates-dev-policy-data" {
    statement {
        effect    = "Allow"
        actions   = ["kms:*"]
        resources = [
            "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/integrates-dev-*"
            ]
    }

}

resource "aws_iam_user" "integrates-dev" {
 name = "integrates-dev"
 path = "/user-provision/"
}

resource "aws_iam_access_key" "integrates-dev-key" {
    user = aws_iam_user.integrates-dev.name
}

resource "aws_iam_user_policy" "integrates-user-policies" {
    name   = "user-provision-policy-${aws_iam_user.integrates-dev.name}"
    user   = aws_iam_user.integrates-dev.name
    policy = data.aws_iam_policy_document.integrates-dev-policy-data.json
}
