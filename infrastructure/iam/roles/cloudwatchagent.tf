data "aws_iam_policy_document" "fs-cloudwatchagent-doc" {
  statement {
    sid = "FSCloudWatchAgent"
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

data "aws_iam_policy_document" "fs-cloudwatchagent-assume-role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "fs-cloudwatchagent" {
  name        = "FS_CloudWatch_Agent"
  path        = "/"
  description = "Role to enable custom metrics in EC2 instances"
  
  assume_role_policy = "${data.aws_iam_policy_document.fs-cloudwatchagent-assume-role.json}"
}

resource "aws_iam_role_policy" "fs-cloudwatchagent-policy" {
  name   = "FS_CloudWatch_Agent_Policy"
  policy = "${data.aws_iam_policy_document.fs-cloudwatchagent-doc.json}"
  role   = "${aws_iam_role.fs-cloudwatchagent.name}"
}
