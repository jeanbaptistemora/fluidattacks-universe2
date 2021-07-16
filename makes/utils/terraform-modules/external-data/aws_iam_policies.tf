variable "aws_iam_policies" {
  type    = map(tuple([string, string]))
  default = {}
  validation {
    condition     = !contains([for k, v in var.aws_iam_policies : contains(["aws", "us"], v[0])], false)
    error_message = "Type must be one of: aws, us."
  }
}

data "aws_iam_policy" "aws_iam_policies" {
  for_each = var.aws_iam_policies
  arn = (
    each.value[0] == "aws"
    ? "arn:aws:iam::aws:policy/${each.value[1]}"
    : (
      each.value[0] == "us"
      ? "arn:aws:iam::${data.aws_caller_identity.me.account_id}:policy/${each.value[1]}"
      : null
    )
  )
}

output "aws_iam_policies" {
  value = data.aws_iam_policy.aws_iam_policies
}
