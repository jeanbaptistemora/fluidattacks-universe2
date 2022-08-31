config {
  module = true
}
plugin "aws" {
  enabled = true
  deep_check = true
}
rule "aws_resource_missing_tags" {
  enabled = true
  tags = [
    "Name",
    "Management:Area",
    "Management:Product",
    "Management:Type",
  ]
  exclude = [
    "aws_elasticache_subnet_group",
    "aws_iam_instance_profile",
    "aws_iam_policy",
  ]
}
