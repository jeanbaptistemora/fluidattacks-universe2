data "aws_iam_policy_document" "fs-cloudwatchagent-doc" {
  statement {
    sid = "FS_CloudWatch_Agent"
    actions = [
      "cloudwatch:PutMetricData",
      "ec2:DescribeTags",
      "logs:PutLogEvents",
      "logs:DescribeLogStreams",
      "logs:DescribeLogGroups",
      "logs:CreateLogStream",
      "logs:CreateLogGroup"
    ]
    resources = [
      "*"
    ]
  }
  statement {
    actions = [
      "ssm:GetParameter"
    ]
    resources = [
      "arn:aws:ssm:*:*:parameter/AmazonCloudWatch-*"
    ]
  }
}

resource "aws_iam_role" "fs-cloudwatchagent" {
  name        = "FS_CloudWatch_Agent"
  path        = "/"
  description = "Role to enable custom metrics in EC2 instances"
  
  assume_role_policy = "${data.aws_iam_policy_document.fs-cloudwatchagent-doc.json}"
}