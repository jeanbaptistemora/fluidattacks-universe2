data "aws_iam_policy_document" "autoscaling_ci_policy_document_data" {

  # https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/index.html#aws-credentials

  statement {
    sid = "AutoscalingCIFullEC2Access"
    effect = "Allow"
    actions = [
      "ec2:*"
    ]
    resources = [
      "*"
    ]
  }

  statement {
      sid = "AutoscalingCIFullS3CacheAccess"
      effect = "Allow"
      actions = [
        "s3:*"
      ]
      resources = [
        "arn:aws:s3:::${var.autoscaling_ci_s3_cache_bucket}/*"
      ]
    }

}

resource "aws_iam_policy" "autoscaling_ci_policy" {
  name        = "autoscaling-ci-policy"
  path        = "/autoscaling-ci/"
  description = "Policy to allow the Bastion to manage EC2 and S3 Cache bucket"

  policy = "${data.aws_iam_policy_document.autoscaling_ci_policy_document_data.json}"
}

resource "aws_iam_user" "autoscaling_ci_user" {
  name     = "autoscaling-ci"
  path     = "/autoscaling-ci/"
}

resource "aws_iam_user_policy_attachment" "attach_autoscaling_ci_policy" {
  policy_arn = "${aws_iam_policy.autoscaling_ci_policy.arn}"
  user       = "${aws_iam_user.autoscaling_ci_user.name}"
}
