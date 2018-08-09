resource "aws_iam_policy_attachment" "web-attach" {
  name       = "web-attachment"
  groups     = ["${var.web}"]
  policy_arn = "${aws_iam_policy.Blog_IAM_Policy.arn}"
}

resource "aws_iam_policy_attachment" "FI_S3INTEGRATION-attach" {
  name       = "FI_S3INTEGRATION-attachment"
  groups     = ["${var.fis3integration}"]
  policy_arn = "${aws_iam_policy.FI_S3INTEGRATION.arn}"
}

resource "aws_iam_policy_attachment" "dynamo-attach" {
    name       = "FluidIntegrates_DynamoDB_Attachment"
    groups     = ["${var.fiDynamo}"]
    policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_policy_attachment" "fluidserves-attach" {
  name       = "fluidserves-attachment"
  groups     = ["${var.fluidserves}"]
  policy_arn = "${aws_iam_policy.fluidserves.arn}"
}

resource "aws_iam_policy_attachment" "SSO_Finance-attach" {
  name       = "SSO_Finance-attachment"
  roles     = ["${var.ssofinance}"]
  policy_arn = "${aws_iam_policy.SSO_Finance.arn}"
}
