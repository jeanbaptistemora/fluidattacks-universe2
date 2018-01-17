resource "aws_iam_policy" "CloudFormation_Lambda" {
  name        = "CloudFormation_Lambda"
  path        = "/"
  description = ""
  policy      = "${file("iam/cloudformation_lambda.json")}"
}
