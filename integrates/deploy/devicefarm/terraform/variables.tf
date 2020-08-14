data "aws_caller_identity" "current" {}
data "aws_iam_policy_document" "device-farm" {

  statement {
    sid    = "Device farm"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/integrates-prod",
      ]
    }
    actions = [
      "devicefarm:CreateProject",
    ]
    resources = [
      "*"
    ]
  }
}

/**
 * Device farm currently only supports us-west-2
 * https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/
 */
variable "region" {
  default = "us-west-2"
}
variable "aws_access_key" {}
variable "aws_secret_key" {}
