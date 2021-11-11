
data "aws_arn" "root" {
  arn = "arn:aws:iam::${data.aws_caller_identity.me.account_id}:root"
}

data "aws_caller_identity" "me" {}

output "aws_me" {
  value = data.aws_caller_identity.me
}

output "aws_root" {
  value = data.aws_arn.root
}
