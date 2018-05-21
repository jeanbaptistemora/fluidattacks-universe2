output "ssofinance" {
  value = "${aws_iam_role.SSO_Finance.name}"
}

output "fs-cloudwatchagent-role" {
  value = "${aws_iam_role.fs-cloudwatchagent.name}"
}