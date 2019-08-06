data "aws_iam_policy_document" "ssofinance-policy" {
  statement {
    sid = "Stmt1450111320000"
    effect = "Allow"
    actions = [
      "ec2:StartInstances",
      "ec2:StopInstances"
    ]
    resources = [
      "arn:aws:ec2:us-east-1:205810638802:instance/i-0ba149836e9bb8e7c"
    ]
  }
}


resource "aws_iam_policy" "SSO_Finance" {
  name        = "SSO_Finance"
  path        = "/"
  description = "Policy for SSO_Finance"

  policy = "${data.aws_iam_policy_document.ssofinance-policy.json}"
}

resource "aws_iam_policy_attachment" "SSO_Finance-attach" {
  name       = "SSO_Finance-attachment"
  roles     = ["${var.ssofinance}"]
  policy_arn = "${aws_iam_policy.SSO_Finance.arn}"
}
