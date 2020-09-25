config {
  module = true
  deep_check = true
}

rule "aws_resource_missing_tags" {
  enabled = true
  tags = [
    "management:type",
    "management:product",
  ]
}
