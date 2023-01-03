resource "aws_iam_role" "safe_role_1" {
  name = "safe_role_1"
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSIoTLogging",
    "arn:aws:iam::aws:policy/AWSAgentlessDiscoveryService"
  ]
}

resource "aws_iam_role" "vuln_role_1" {
  name = "vuln_role_1"

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/AdministratorAccess"
  ]
}
