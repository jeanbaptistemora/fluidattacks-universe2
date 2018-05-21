variable "fs-cloudwatchagent-role" {}

resource "aws_iam_instance_profile" "fs-cloudwatchagent" {
  name = "FS_CloudWatch_Agent"
  path = "/"
  role = "${var.fs-cloudwatchagent-role}"
}