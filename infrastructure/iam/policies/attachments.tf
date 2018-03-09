resource "aws_iam_policy_attachment" "web-attach" {
  name       = "web-attachment"
  groups     = ["web"]
  policy_arn = "${aws_iam_policy.Blog_IAM_Policy.arn}"
}

resource "aws_iam_policy_attachment" "cflambda-attach" {
  name       = "cflambda-attachment"
  groups     = ["LambdaCallers"]
  policy_arn = "${aws_iam_policy.CloudFormation_Lambda.arn}"
}

resource "aws_iam_policy_attachment" "FI_S3INTEGRATION-attach" {
  name       = "FI_S3INTEGRATION-attachment"
  groups     = ["FI_S3INTEGRATION"]
  policy_arn = "${aws_iam_policy.FI_S3INTEGRATION.arn}"
}

resource "aws_iam_policy_attachment" "fluidserves-attach" {
  name       = "fluidserves-attachment"
  groups     = ["fluidserves"]
  policy_arn = "${aws_iam_policy.fluidserves.arn}"
}

resource "aws_iam_policy_attachment" "fluidstores-attach" {
  name       = "fluidstores-attachment"
  groups     = ["fluidstores"]
  policy_arn = "${aws_iam_policy.fluidstores.arn}"
}

resource "aws_iam_policy_attachment" "SSO_Finance-attach" {
  name       = "SSO_Finance-attachment"
  roles     = ["SSO_Finance"]
  policy_arn = "${aws_iam_policy.SSO_Finance.arn}"
}
